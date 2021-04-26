import os
import json

import logging as logger
import re

from osbot_utils.utils.Files import create_folder
from osbot_utils.utils.Json import json_save_file_pretty, json_load_file
from cdr_plugin_folder_to_folder.common_settings.Config import Config
from cdr_plugin_folder_to_folder.pre_processing.Status import FileStatus

from enum import Enum

from cdr_plugin_folder_to_folder.storage.Storage import Storage
from cdr_plugin_folder_to_folder.utils.Logging import log_error
from cdr_plugin_folder_to_folder.utils._to_refactor.For_OSBot_Utils.Misc import is_regex_full_match

logger.basicConfig(level=logger.INFO)


class Analysis_Json:

    ANALYSIS_FILE_NAME = "analysis.json"
    REGEX_HASH     = '[A-Fa-f0-9]{64}$'

    def __init__(self):
        self.config  = Config()
        self.storage = Storage()
        self.folder  = os.path.join(self.config.hd2_location, "status")
        self.analysis_data    = {}
        self.id      = 0
        self.get_from_file()

    def is_hash(self, value):
        return is_regex_full_match(Analysis_Json.REGEX_HASH, value)

    def add_file(self, file_hash, file_name):
        if self.is_hash(file_hash) and file_name:
            json_value  = {"file_name"  : file_name}

            json_data   = {file_hash: json_value}

            self.analysis_data.update(json_data)
            self.write_to_file()
            return True
        log_error(message='in Analysis_Json.add_file bad data provided', data = {'file_hash': file_hash, 'file_name': file_name})
        return False

    def get_file_path(self):
        return os.path.join(self.folder, Analysis_Json.ANALYSIS_FILE_NAME)

    def get_from_file(self):
        self.analysis_data = json_load_file(self.get_file_path())
        return self.analysis_data

    def write_to_file(self):
        create_folder(self.folder)
        json_save_file_pretty(self.analysis_data, self.get_file_path())

    def update_report(self, index, report_json):
        try:
            self.get_from_file()

            self.analysis_data[index]["file_type"]                  = report_json["gw:GWallInfo"]["gw:DocumentStatistics"]["gw:DocumentSummary"]["gw:FileType"]
            self.analysis_data[index]["file_size"]                  = report_json["gw:GWallInfo"]["gw:DocumentStatistics"]["gw:DocumentSummary"]["gw:TotalSizeInBytes"]

            self.analysis_data[index]["remediated_item_count"], \
            self.analysis_data[index]["remediate_items_list"]       = self.get_remediated_item_details(report_json)

            self.analysis_data[index]["sanitised_item_count"], \
            self.analysis_data[index]["sanitised_items_list"]       = self.get_sanitisation_item_details(report_json)

            self.analysis_data[index]["issue_item_count"],\
            self.analysis_data[index]["issue_item_list"]            = self.get_issue_item_details(report_json)

            self.write_to_file()
        except Exception as error:
            log_error(message=f"Error in update_report from json data {index} : {error}")

    def get_remediated_item_details(self, report_json):
        total_remediate_count = 0
        remediate_items_list  = []

        for item in report_json["gw:GWallInfo"]["gw:DocumentStatistics"]["gw:ContentGroups"]["gw:ContentGroup"]:
            remediate_count=int(item["gw:RemedyItems"]["@itemCount"])
            total_remediate_count = total_remediate_count + remediate_count
            if "gw:RemedyItem" in item["gw:RemedyItems"] and remediate_count > 0:

                if "gw:TechnicalDescription" in item["gw:RemedyItems"]["gw:RemedyItem"]:
                    remediate_items_list.append(item["gw:RemedyItems"]["gw:RemedyItem"]["gw:TechnicalDescription"])
                else:
                    for remediate_item in item["gw:RemedyItems"]["gw:RemedyItem"]:
                        remediate_items_list.append(remediate_item["gw:TechnicalDescription"])

        return total_remediate_count, remediate_items_list

    def get_sanitisation_item_details(self, report_json):
        total_sanitisation_count = 0
        sanitisation_items_list  = []

        for item in report_json["gw:GWallInfo"]["gw:DocumentStatistics"]["gw:ContentGroups"]["gw:ContentGroup"]:
            sanitisation_count=int(item["gw:SanitisationItems"]["@itemCount"])
            total_sanitisation_count = total_sanitisation_count + sanitisation_count

            if "gw:SanitisationItem" in item["gw:SanitisationItems"] and sanitisation_count > 0:

                if "gw:TechnicalDescription" in item["gw:SanitisationItems"]["gw:SanitisationItem"]:
                    sanitisation_items_list.append(
                        item["gw:SanitisationItems"]["gw:SanitisationItem"]["gw:TechnicalDescription"])
                else:
                    for sanitisation_item in item["gw:SanitisationItems"]["gw:SanitisationItem"]:
                        sanitisation_items_list.append(sanitisation_item["gw:TechnicalDescription"])

        return total_sanitisation_count, sanitisation_items_list

    def get_issue_item_details(self, report_json):
        total_issue_count  = 0
        issue_items_list   = []

        for item in report_json["gw:GWallInfo"]["gw:DocumentStatistics"]["gw:ContentGroups"]["gw:ContentGroup"]:
            issue_count=int(item["gw:IssueItems"]["@itemCount"])
            total_issue_count = total_issue_count + issue_count
            if "gw:IssueItem" in item["gw:IssueItems"] and issue_count > 0:

                if "gw:TechnicalDescription" in item["gw:IssueItems"]["gw:IssueItem"]:
                    issue_items_list.append(item["gw:IssueItems"]["gw:IssueItem"]["gw:TechnicalDescription"])
                else:
                    for issue_item in item["gw:IssueItems"]["gw:IssueItem"]:
                        issue_items_list.append(issue_item["gw:TechnicalDescription"])

        return total_issue_count, issue_items_list
