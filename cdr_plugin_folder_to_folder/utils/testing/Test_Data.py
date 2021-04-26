from osbot_utils.utils.Files import path_combine, files_list, file_contents_as_bytes, file_create_bytes
from osbot_utils.utils.Misc import list_filter, str_to_bytes, random_text


class Test_Data:

    def __init__(self):
        self.path_test_files = path_combine(__file__, '../../../../test_data/scenario-2/hd1')

    def files(self):
        files = files_list(self.path_test_files)
        return list_filter(files, lambda x: x.find('.DS_Store') == -1)      # todo: add better method to OSBot-utils

    def json(self):
        return self.jsons().pop()

    def jsons(self):
        return files_list(self.path_test_files,"*.json")

    def image(self):
        return self.images().pop()

    def images(self):
        return files_list(self.path_test_files,"*.jpg")

    def pdfs(self):
        return files_list(self.path_test_files, "*.jpg")

    def create_test_pdf(self, text=None, file_key=None):
        # see https://brendanzagaeski.appspot.com/0004.html for a description of the code bellow
        text = text or random_text(prefix="Some random text in Arial : ")
        font = "Arial" # "Times-Roman"
        # todo: format the pdf text below better
        small_pdf_bytes = str_to_bytes( '%PDF-1.1\n%\xc2\xa5\xc2\xb1\xc3\xab\n\n1 0 obj\n  << /Type /Catalog\n     /'
                                        'Pages 2 0 R\n  >>\nendobj\n\n2 0 obj\n  << /Type /Pages\n     /Kids [3 0 R'
                                        ']\n     /Count 1\n     /MediaBox [0 0 300 144]\n  >>\nendobj\n\n3 0 obj\n  '
                                        '<<  /Type /Page\n      /Parent 2 0 R\n      /Resources\n       << /Font\n   '
                                        '        << /F1\n               << /Type /Font\n                  /Subtype '
                                       f'/Type1\n                  /BaseFont /{font}\n               >>\n      '
                                        '     >>\n       >>\n      /Contents 4 0 R\n  >>\nendobj\n\n4 0 obj\n  << /L'
                                       f'ength 55 >>\nstream\n  BT\n    /F1 18 Tf\n    0 0 Td\n    ({text}) T'
                                        'j\n  ET\nendstream\nendobj\n\nxref\n0 5\n0000000000 65535 f \n0000000018 000'
                                        '00 n \n0000000077 00000 n \n0000000178 00000 n \n0000000457 00000 n \ntraile'
                                        'r\n  <<  /Root 1 0 R\n      /Size 5\n  >>\nstartxref\n565\n%%EOF\n')

        file_key = file_key or "test"
        return file_create_bytes(extension=file_key + '.pdf',contents=small_pdf_bytes)