#!/usr/bin/python3

import argparse
import allitebooks
import conf
import downloader
import file_mgt
from file_mgt import DumpFileManager
from library import Library, LibrarySearchView

parser = argparse.ArgumentParser()
parser.add_argument('search', nargs='+', help='the book search keywords as you would type them on the allitebooks site')
parser.add_argument('-q', '--quiet', action='store_true', default=False,
                    help='do not display information about the download')
args = parser.parse_args()

search = '+'.join(args.search)
verbose_mode = not args.quiet

dump_file_manager = DumpFileManager(conf.scrapper[conf.dl_link_dump_path])
dl_links = None

if dump_file_manager.dump_file_exists(search):
    user_input = None
    while user_input not in ['y', 'n']:
        user_input = input('The link search has already been made, do you want to use it ? [y/n] ')
    if user_input == 'y':
        dl_links = dump_file_manager.get_dl_links_from_dump(search)
    else:
        dump_file_manager.remove_dump_file(search)

if dl_links is None:
    dl_links = allitebooks.get_dl_links(search)
    dump_file_manager.dump_dl_links(search, dl_links)

library_ = Library(conf.scrapper[conf.library_path], conf.scrapper[conf.managed_extensions])
library_search_view = LibrarySearchView(library_, search)
library_search_view.analyse(dl_links)

nb_of_already_in_lib_books = len(library_search_view.already_in_library_books)
if nb_of_already_in_lib_books > 0 and verbose_mode:
    print(
        'You have already {} books out of {} results in your library'.format(nb_of_already_in_lib_books, len(dl_links)))

nb_of_books_to_dl = len(library_search_view.to_dl_links)
if nb_of_books_to_dl > 0:
    user_input = None
    while user_input not in ['y', 'n']:
        user_input = input(
            'You are about to download {} books, do you want to proceed ? [y/n] '.format(nb_of_books_to_dl))
    if user_input == 'y':
        file_mgt.create_dir(library_search_view.storage_dir_path)
        errors_at_dl_time = downloader.mass_download(library_search_view.to_dl_links,
                                                     library_search_view.storage_dir_path,
                                                     verbose_mode)
        library_search_view.create_dummy_books(conf.scrapper[conf.dummy_books_extension])

        nb_errors = len(errors_at_dl_time)
        if nb_errors > 0 and verbose_mode:
            print('There were {} errors at dl time'.format(nb_errors))
    elif verbose_mode:
        print('Aborted')
elif verbose_mode:
    print('No book to dl')
