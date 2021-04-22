import sys
import json
import requests
import ntpath
import os.path
import xmltodict

from osbot_utils.utils.Files import folder_create
from osbot_utils.utils.Json import json_save_file_pretty
from datetime import datetime, timedelta

from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.utils.Log_Duration import log_duration
from cdr_plugin_folder_to_folder.utils.Logging import log_error
from cdr_plugin_folder_to_folder.utils.file_utils import FileService
from cdr_plugin_folder_to_folder.metadata.Metadata_Service import Metadata_Service
from cdr_plugin_folder_to_folder.processing.Events_Log import Events_Log
from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.pre_processing.Status import Status
from cdr_plugin_folder_to_folder.processing.Report_Elastic import Report_Elastic

class File_Processing:

    def __init__(self, events_log, report_elastic, meta_service):
        self.meta_service   = meta_service
        self.events_log     = events_log
        self.storage        = Storage()
        self.config         = Config()
        self.status         = Status()
        self.report_elastic = report_elastic

    def base64request(self, endpoint, api_route, base64enc_file):
        try:
            url = endpoint + "/" + api_route

            payload = json.dumps({
              "Base64": base64enc_file
            })

            headers = {
              'Content-Type': 'application/json'
            }

            return requests.request("POST", url, headers=headers, data=payload, timeout=self.config.request_timeout)
     
        except Exception as e:
            log_error(str(e))
            raise ValueError(str(e))

    def xmlreport_request(self, endpoint, fileID):
        try:
            url = endpoint + "/api/Analyse/xmlreport?fileId=" + fileID

            payload = ""
            headers = {
                'Content-Type': 'application/octet-stream'
            }

            response = requests.request("GET", url, headers=headers, data=payload, timeout=self.config.request_timeout)
            return response.text

        except Exception as e:
            raise ValueError(str(e))

    def rebuild (self, endpoint, base64enc_file):
        return self.base64request(endpoint, "api/rebuild/base64", base64enc_file)

    def get_xmlreport(self, endpoint, fileId, dir):
        xmlreport = self.xmlreport_request(endpoint, fileId)
        if not xmlreport:
            raise ValueError('Failed to obtain the XML report')

        json_obj = xmltodict.parse(xmlreport)
        json_obj['original_hash'] = os.path.basename(dir)
        json_save_file_pretty(json_obj, os.path.join(dir, "report.json"))

        self.report_elastic.add_report(json_obj)

    # Save to HD3
    def save_file(self, result, processed_path):
        self.events_log.add_log('Saving to: ' + processed_path)

        dirname = ntpath.dirname(processed_path)
        basename = ntpath.basename(processed_path)
        folder_create(dirname)

        decoded = FileService.base64decode(result)

        if decoded:
            FileService.wrtie_binary_file(dirname, basename, decoded)
            self.events_log.add_log('The decoded file has been saved')
        else:
            FileService.wrtie_file(dirname, basename + ".html", result)
            self.events_log.add_log('Decoding FAILED. The HTML file has been saved')

    @log_duration
    def do_rebuild(self, endpoint, hash, source_path, dir):

        self.meta_service.set_rebuild_server(dir, endpoint)

        file_size = os.path.getsize(source_path)
        self.meta_service.set_original_file_size(dir, file_size)

        encodedFile = FileService.base64encode(source_path)
        if not encodedFile:
            self.events_log.add_log("Failed to encode the file")
            raise ValueError("Failed to encode the file")

        response = self.rebuild(endpoint, encodedFile)
        result = response.text
        if not result:
            self.events_log.add_log('Failed to rebuild the file')
            raise ValueError('Failed to rebuild the file')

        for path in self.meta_service.get_original_file_paths(dir):
            rebuild_file_path = path
            if path.startswith(self.config.hd1_location):
                rebuild_file_path = path.replace(self.config.hd1_location, self.config.hd3_location)
            else:
                rebuild_file_path = os.path.join(self.config.hd3_location, path)

            self.save_file(result, rebuild_file_path)
            file_size = os.path.getsize(rebuild_file_path)
            self.meta_service.set_rebuild_file_size(dir, file_size)
            self.meta_service.set_rebuild_file_path(dir, rebuild_file_path)
            rebuild_hash = self.meta_service.file_hash(rebuild_file_path)
            self.meta_service.set_rebuild_hash(dir, rebuild_hash)

        headers = response.headers
        fileIdKey = "X-Adaptation-File-Id"

        # get XML report
        if fileIdKey in headers:
            self.get_xmlreport(endpoint, headers[fileIdKey], dir)
            self.events_log.add_log('The XML report has been saved')
            self.meta_service.set_xml_report_status(dir, "Obtained")
        else:
            self.events_log.add_log('No X-Adaptation-File-Id header found in the response')
            raise ValueError("No X-Adaptation-File-Id header found in the response")
            self.meta_service.set_xml_report_status(dir, "Failed to obtain")

    @log_duration
    def processDirectory (self, endpoint, dir):
        self.events_log.add_log("Processing Directory: " + dir)
        hash = ntpath.basename(dir)
        if len(hash) != 64:
            self.events_log.add_log("Unexpected hash length")
            raise ValueError("Unexpected hash length")

        metadata_file_path = os.path.join(dir, Metadata_Service.METADATA_FILE_NAME)
        if not (FileService.file_exist(metadata_file_path)):
            self.events_log.add_log("The metadate.json file does not exist")
            raise ValueError("The metadate.json file does not exist")

        if not self.meta_service.is_initial_status(dir):
            self.events_log.add_log("Metadata not in the INITIAL state")
            return False

        self.meta_service.set_status_inprogress(dir)
        self.status.add_in_progress()

        source_path = os.path.join(dir, "source")
        if not (FileService.file_exist(source_path)):
            self.events_log.add_log("File does not exist")
            raise ValueError("File does not exist")

        self.events_log.add_log("Sending to rebuild")
        tik = datetime.now()
        self.do_rebuild(endpoint, hash, source_path, dir)
        tok = datetime.now()
        delta = tok - tik
        self.meta_service.set_rebuild_file_duration(dir, str(delta))

        return True
