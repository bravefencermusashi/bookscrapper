import re

from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import logging


def get_soup_from_url(url):
    response = urllib.request.urlopen(url)
    return BeautifulSoup(response.read().decode(), 'lxml')


class AllItEbooksException(Exception):
    pass


class WebPage:
    def __init__(self, url):
        self.url = url
        self.soup = None

    def _get_soup(self):
        if self.soup is None:
            self.soup = get_soup_from_url(self.url)

        return self.soup


class AllItEbooksBookPage(WebPage):
    def get_book_dl_link(self):
        dl_link_tags = self._get_soup().find_all(href=re.compile("pdf$"))
        if len(dl_link_tags) != 1:
            raise AllItEbooksException()
        else:
            book_dl_link = dl_link_tags[0]['href']

        return book_dl_link


class AllItEbooksSearchPage(WebPage):
    def __init__(self, search, page_number):
        WebPage.__init__(self, 'http://www.allitebooks.com/page/{}/?s={}'.format(page_number, search))

    def get_number_of_search_pages(self):
        number_of_pages = 1
        page_link_tags = self._get_soup().find_all(href=re.compile("page"))
        if len(page_link_tags) > 1:
            match = re.search('page/(\d+)/', page_link_tags[-1]['href'])
            if match:
                number_of_pages = int(match.group(1))
            else:
                logging.debug('no page link found')
        return number_of_pages

    def _get_book_page_urls_as_set(self):
        book_page_url_set = set()
        for book_link_tag in self._get_soup().find_all('a', rel="bookmark"):
            book_page_url_set.add(book_link_tag['href'])
        return book_page_url_set

    def get_book_pages(self):
        book_page_urls_set = self._get_book_page_urls_as_set()
        book_pages = list()
        for book_page_url in book_page_urls_set:
            book_pages.append(AllItEbooksBookPage(book_page_url))
        return book_pages


def get_dl_links_of_page(search, page_number):
    search_page = AllItEbooksSearchPage(search, page_number)
    book_pages = search_page.get_book_pages()
    dl_links_of_page_books = list()
    for bp in book_pages:
        try:
            dl_links_of_page_books.append(bp.get_book_dl_link())
        except AllItEbooksException:
            logging.warning('could not retrieve book dl link from {} -- SKIPPED'.format(bp.url))

    return dl_links_of_page_books


def get_dl_links(search):
    search_page = AllItEbooksSearchPage(search, 1)
    number_of_search_pages = search_page.get_number_of_search_pages()
    dl_links_list = list()
    for page in range(1, number_of_search_pages + 1):
        for dl_link in get_dl_links_of_page(search, page):
            dl_links_list.append(dl_link)

    return dl_links_list
