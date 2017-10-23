import os

import downloader
import file_mgt


class Library:
    def __init__(self, library_dir, managed_extensions):
        self.library_dir = library_dir
        self.book_dict = None
        self.managed_extensions = managed_extensions

    def load(self):
        self.book_dict = file_mgt.get_file_names_in_tree(self.library_dir, self.managed_extensions)

    def get_storage_dir_path(self, search: str) -> str:
        return os.path.join(self.library_dir, search)

    def book_in_library(self, book_file_name):
        file_path_if_exists = None
        if book_file_name in self.book_dict:
            file_path_if_exists = os.path.join(self.book_dict[book_file_name], book_file_name)
        return file_path_if_exists


class LibrarySearchView:
    def __init__(self, library: Library, search):
        self.library = library
        self.search = search
        self.to_dl_links = None
        self.already_in_library_books = None
        self.storage_dir_path = self.library.get_storage_dir_path(self.search)

    def analyse(self, dl_links):
        if self.library.book_dict is None:
            self.library.load()
        to_dl_links = list()
        already_in_library_books = dict()
        for dl_link in dl_links:
            file_name = downloader.retrieve_file_name_from_download_url(dl_link)
            book_path_if_exists = self.library.book_in_library(file_name)
            if book_path_if_exists is None:
                to_dl_links.append(dl_link)
            else:
                already_in_library_books[file_name] = book_path_if_exists
        self.to_dl_links = to_dl_links
        self.already_in_library_books = already_in_library_books

    def create_dummy_books(self, dummy_ext=None):
        for file_name, full_path in self.already_in_library_books.items():
            file_name_without_ext = file_mgt.get_file_name_without_extension(file_name)
            if not full_path.startswith(self.storage_dir_path):
                if dummy_ext is None:
                    final_file_name = file_name_without_ext
                else:
                    final_file_name = file_mgt.add_ext_to_file_name(file_name_without_ext, dummy_ext)
                file_mgt.create_or_override_file(os.path.join(self.storage_dir_path, final_file_name), full_path)
