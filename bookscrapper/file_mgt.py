import json
import os
import re


def get_file_names_in_tree(dir_to_scan: str, extension_filter: list = None) -> dict:
    file_names_dict = dict()
    pattern = re.compile('\.(\w+)$')
    for dirpath, _, file_names in os.walk(dir_to_scan):
        for file_name in file_names:
            if extension_filter is None:
                file_names_dict[file_name] = dirpath
            else:
                match = re.search(pattern, file_name)
                if match and match.group(1) in extension_filter:
                    file_names_dict[file_name] = dirpath
    return file_names_dict


def get_file_name_without_extension(file_name: str):
    return file_name.rsplit('.', maxsplit=1)[0]


def add_ext_to_file_name(file_name, ext):
    return '{}.{}'.format(file_name, ext)


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def create_or_override_file(path: str, str_content: str):
    if os.path.exists(path):
        if os.path.isdir(str_content):
            raise OSError('{} is a directory, give a path to a file'.format(path))
    with open(path, 'w') as file:
        file.write(str_content)


def create_dir_on_user_request(path, desc=''):
    was_created = False
    if not os.path.exists(path):
        user_input = None
        if desc != '':
            desc = ' ({})'.format(desc)
        question = 'The following directory does not exist {}{}. Do you want to create it ? [y/n] '.format(path, desc)
        while user_input not in ['y', 'n']:
            user_input = input(question)
        if user_input == 'y':
            os.makedirs(path)
            was_created = True

    return was_created


class DumpFileManager:
    def __init__(self, dump_files_directory_path):
        self.dump_files_directory_path = dump_files_directory_path

    @staticmethod
    def get_dump_file_name(search):
        return 'dl_links_dump_{}'.format(search)

    def get_dump_file_path(self, search):
        return os.path.join(self.dump_files_directory_path, self.get_dump_file_name(search))

    @staticmethod
    def get_dl_links_from_dump_file_path(path):
        if os.path.exists(path):
            with open(path, 'r') as dump_file:
                dl_links = json.load(dump_file)
        else:
            raise OSError('file {} does not exists'.format(path))
        return dl_links

    def get_dl_links_from_dump(self, search):
        dump_file_path = self.get_dump_file_path(search)
        return self.get_dl_links_from_dump_file_path(dump_file_path)

    def dump_dl_links(self, search, dl_links):
        dump_file_path = self.get_dump_file_path(search)
        with open(dump_file_path, 'w') as dump_file:
            json.dump(dl_links, dump_file)

    def dump_file_exists(self, search):
        dump_file_path = self.get_dump_file_path(search)
        return os.path.exists(dump_file_path)

    def remove_dump_file(self, search):
        dump_file_path = self.get_dump_file_path(search)
        os.remove(dump_file_path)
