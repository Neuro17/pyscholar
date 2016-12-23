# -*- coding: utf-8 -*-

import urllib2
import cookielib
import logging

from bs4 import BeautifulSoup
from urllib import urlencode

SCHOLAR_SITE = 'https://scholar.google.it'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) ' \
             'Gecko/2009021910 Firefox/3.0.7'
MAX_PAGES = 1

class Query:

    def __init__(self, words='', phrase='', authors='', words_some='',
                 words_none='', citations=''):

        # this param is equivalent to the button "see all results"
        self.lookup = 0
        self.words = words
        self.phrase = phrase
        self.authors = authors
        self.words_some = words_some
        self.words_none = words_none
        self.citations = citations
        self._query = None
        self.language = 'en'

    def _quote(self):
        for attr in [a for a in vars(self) if not a.startswith('_')]:
            attr_value = getattr(self, attr)
            if isinstance(attr_value, list):
                setattr(self, attr, ' '.join(attr_value))

    def build(self):
        self._quote()
        self._query = {'lookup': self.lookup,
                       'as_q': self.words,
                       'as_epq': self.phrase,
                       'as_sauthors': self.authors,
                       'as_oq': self.words_some,
                       'as_eq': self.words_none,
                       'as_vis': self.citations,
                       'hl': self.language}
        return SCHOLAR_SITE + '/scholar?' + urlencode(self._query)


class Article:

    def __init__(self, title=None, url=None, citations=None, citations_url=None,
                 year=None, authors=None, pdf_link=None):
        self.title = title
        self.url = url
        self.citations = int(citations) if citations else None
        self.citations_url = citations_url
        self.year = year
        self.authors = authors
        self.pdf_link = pdf_link

    def __str__(self):
        pass #TODO: override __str__ method

    def to_dict(self):
        return vars(self)


class Parser:

    def __init__(self, log_level=logging.DEBUG):
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(level=log_level)

    def parse(self, page):
        articles = []
        records = page.find_all('div', {'class': 'gs_r'})
        for record in records:
            articles.append(self._parse_scholar_record(record))
        return articles

    def _extract_title_info(self):
        pass

    def _extract_publication_info(self):
        pass

    def _extract_citation_info(self):
        pass

    def _extract_pdf_info(self):
        pass

    def _extract_bib_info(self):
        pass

    def _parse_scholar_record(self, record):
        article = record.select('div.gs_ri')
        if not article:
            return
        else:
            article = article[0]
        title_info = article.select('h3.gs_rt a')
        if title_info:
            title = title_info[0].text
            title_link = title_info[0].get('href')

            publication_info = article.select('div.gs_a')
            # AW Lo, H Mamaysky, J Wang - The journal of finance, 2000
            # - Wiley Online Library
            self._logger.debug(publication_info)
            authors = publication_info[0].text.split('-')[0].split(',')
            cites_info = article.select('div.gs_fl a:nth-of-type(1)')
            num_cites = cites_info[0].text.split(' ')[2]  # Cited by 988
            cites_link = cites_info[0].get('href')
            pdf_info = record.select('div.gs_ggsd a')
            pdf_link = pdf_info[0].get('href') if pdf_info else 'pdf not found'
            article_tmp = Article(title=title, citations=num_cites,
                                  url=title_link, citations_url=cites_link,
                                  authors=authors, pdf_link=pdf_link)
            return article_tmp


class Crawler:

    def __init__(self, query, pages=None, log_level=logging.DEBUG):
        self._handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
        ]
        self._opener = urllib2.build_opener(*self._handlers)
        self.pages = pages or MAX_PAGES
        self._headers = {'User-Agent': USER_AGENT}
        self._query = query.build()
        self._parser = Parser()
        self._logger = logging.getLogger(__name__)
        self.articles = []
        logging.basicConfig(level=log_level)

    def _get_next_page_url(self, next_page):
        return SCHOLAR_SITE + next_page

    def explore_pages(self):
        def loop(page_number, query):
            if page_number > self.pages:
                return
            self._logger.debug('Exploring ' + query)
            request = urllib2.Request(query, None, self._headers)
            page = BeautifulSoup(self._opener.open(request).read(), 'lxml')

            self.articles += self._parser.parse(page)

            next_page = page.select('div#gs_n center table tr td')[-1:][0] \
                .select('a')[0].get('href')
            self._logger.debug('Next page is ' + \
                               self._get_next_page_url(next_page))

            loop(page_number+1, self._get_next_page_url(next_page))
        loop(1, self._query)

if __name__ == '__main__':
    import pprint as pp
    q = Query(words='mesos')
    print q.build()
    c = Crawler(q, pages=1)
    c.explore_pages()
    for art in c.articles[:1]:
        # print art
        art.year = '2016'
        pp.pprint( art.to_dict())
