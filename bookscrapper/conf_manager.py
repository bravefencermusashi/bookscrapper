import json
import os.path

from bookscrapper import file_mgt

conf_file_name = '.bookscrapper'

dl_link_dump_path = 'dl_link_dump_path'
managed_extensions = 'managed_extensions'
dummy_books_extension = 'dummy_books_extension'
library_path = 'library_path'

library_path_desc = 'library path, where books are stored'
dl_link_dump_path_desc = 'download link path, where download links from already made searches are stored'


def check_directory_and_create_on_request(path, desc=''):
    is_ok = os.path.exists(path)
    if not is_ok:
        is_ok = file_mgt.create_dir_on_user_request(path, desc)
    if not is_ok:
        if desc != '':
            desc = ' ({})'.format(desc)
        print('the following directory must exist {}{} - check and/or change your configuration'.format(path, desc))
    return is_ok


class BSConf:
    def __init__(self):
        self.conf = BSConf.get_default_conf()

        home_dir_path = os.path.expanduser('~')
        self.conf_path = os.path.join(home_dir_path, conf_file_name)
        if os.path.exists(self.conf_path):
            with open(self.conf_path) as conf_file:
                conf_from_file = json.load(conf_file)
                for key, value in conf_from_file.items():
                    self.conf[key] = value

    def check_conf(self):
        is_ok = check_directory_and_create_on_request(self.conf[library_path], library_path_desc)
        if is_ok:
            is_ok = check_directory_and_create_on_request(self.conf[dl_link_dump_path], dl_link_dump_path_desc)
        return is_ok

    def create_conf_file(self):
        created = False
        if not os.path.exists(self.conf_path):
            file_mgt.create_or_override_file(self.conf_path, json.dumps(self.conf, indent=4))
            created = True
        return created

    @staticmethod
    def get_default_conf():
        defaults = dict()
        home_dir_path = os.path.expanduser('~')
        app_default_dir = os.path.join(home_dir_path, 'bookscrapper')

        defaults[library_path] = os.path.join(app_default_dir, 'library')
        defaults[dl_link_dump_path] = os.path.join(app_default_dir, 'dl_link_dumps')
        defaults[managed_extensions] = ['pdf']
        defaults[dummy_books_extension] = 'txt'

        return defaults


