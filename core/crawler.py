import urllib2
import cookielib
import utils
import logging
from utils import SCHOLAR_SITE
from bs4 import BeautifulSoup
from parser import Parser


class Crawler:

    def __init__(self, query, pages=None, log_level=logging.DEBUG):
        self._handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
        ]
        self._opener = urllib2.build_opener(*self._handlers)
        self.pages = pages or utils.MAX_PAGES
        self._headers = {'User-Agent': utils.USER_AGENT}
        self._query = query.build()
        self._parser = Parser()
        self._logger = logging.getLogger(__name__)
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

            self._parser.parse(page)

            next_page = page.select('div#gs_n center table tr td')[-1:][0] \
                .select('a')[0].get('href')
            self._logger.debug('Next page is ' + \
                               self._get_next_page_url(next_page))

            loop(page_number+1, self._get_next_page_url(next_page))
        loop(1, self._query)

if __name__ == '__main__':
    from query import Query
    q = Query(authors='page')
    c = Crawler(q, pages=2)
    c.explore_pages()
