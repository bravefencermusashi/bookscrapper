import os
import requests
import logging
import re

from requests.exceptions import HTTPError

file_name_in_url_pattern = re.compile(r'/([^/]+)$')


class StrangeUrlException(Exception):
    pass


def retrieve_file_name_from_download_url(url):
    match = re.search(file_name_in_url_pattern, url)
    if match:
        file_name = match.group(1)
    else:
        logging.error("can't retrieve file name for {}".format(url))
        raise StrangeUrlException(url)
    return file_name


def download(url, file_path, verbose_mode=False):
    response = requests.get(url)
    response.raise_for_status()

    if verbose_mode :
        print('downloading file {}'.format(file_path))
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=512):
            file.write(chunk)


def mass_download(urls, dir_path, verbose_mode=False):
    errors = list()
    nb_dls = len(urls)
    for dl_num, url in enumerate(urls):
        try:
            file_name = retrieve_file_name_from_download_url(url)
            if verbose_mode:
                print('download {}/{} - '.format(str(dl_num + 1), nb_dls), end='')
            download(url, os.path.join(dir_path, file_name), verbose_mode)
        except StrangeUrlException:
            logging.warning('could not retrieve file name for url {} -- dl aborted'.format(url))
            errors.append(url)
        except HTTPError as e:
            logging.warning('error when trying to dl {} - {}'.format(url, e))
            errors.append(url)
    return errors
