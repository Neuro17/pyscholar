import urllib2
import urllib
from bs4 import BeautifulSoup
import pprint as pp
import logging
import requests
import cookielib

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) ' \
             'Gecko/2009021910 Firefox/3.0.7'

WEB_ROOT = 'https://scholar.google.it'
SCHOLAR = 'scholar'
LANGUAGE = 'en'
QUERY = 'map reduce'

params = {'hl': LANGUAGE,
          'q': urllib.quote_plus(QUERY)}

# params = {'hl': LANGUAGE,
#           'q': urllib.quote_plus(QUERY)}

# headers = {'User-Agent': USER_AGENT}

# web_query = WEB_ROOT + '/' + SCHOLAR + '?' + urllib.urlencode(params)

# request = urllib2.Request(web_query, None, headers)

# soup = BeautifulSoup(urllib2.urlopen(request).read(), "lxml")

# records = soup.find_all('div', {'class': 'gs_r'})
# print len(records)
# for record in records[:1]:
#
# -----------------------------------------------------------------------------#
#             article               |                  PDF                     #
#                                   |                                          #
# -----------------------------------------------------------------------------#
#

def parse_scholar_page(page):
    records = page.find_all('div', {'class': 'gs_r'})
    for record in records:
        parse_scholar_record(record)

    #--------------------------------------------------------------------------#
    #             article               |                  PDF                 #
    #                                   |                                      #
    #--------------------------------------------------------------------------#

def parse_scholar_record(record):
    article = record.select('div.gs_ri')[0]
    title_info = article.select('h3.gs_rt a')
    if title_info:

        title = title_info[0].text
        title_link = title_info[0].get('href')

        publication_info = article.select('div.gs_a')
        # AW Lo, H Mamaysky, J Wang - The journal of finance, 2000
        # - Wiley Online Library
        authors = publication_info[0].text.split('-')[0].split(',')
        cites_info = article.select('div.gs_fl a:nth-of-type(1)')
        num_cites = cites_info[0].text.split(' ')[2]  # Cited by 988
        cites_link = cites_info[0].get('href')
        pdf_info = record.select('div.gs_ggsd a')
        pdf_info = pdf_info[0].get('href') if pdf_info else 'pdf not found'
        print
        print '#' * 80
        print title
        print title_link
        print authors
        print num_cites
        print cites_link
        print pdf_info
        print '#' * 80
        print

        
def get_url(params):
    return WEB_ROOT + params


def explore_google_pages(google_url, map=None, pages=1):
    headers = {'User-Agent': USER_AGENT}
    # Cookies are needed to avoid error 403 (forbidden), after too many request.
    cookies = cookielib.LWPCookieJar()
    handlers = [
        urllib2.HTTPHandler(),
        urllib2.HTTPSHandler(),
        urllib2.HTTPCookieProcessor(cookies)
    ]
    opener = urllib2.build_opener(*handlers)

    def loop(page_number, url):
        if page_number > pages:
            return
        logger.info('Exploring ' + url)
        request = urllib2.Request(url, None, headers)
        page = BeautifulSoup(opener.open(request).read(), "lxml")

        parse_scholar_page(page)

        # print soup
        next_page = page.select('div#gs_n center table tr td')[-1:][0] \
            .select('a')[0].get('href')

        logging.info(get_url(next_page))

        loop(page_number + 1, get_url(next_page))

    loop(1, google_url)


if __name__ == '__main__':
    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    WEB_ROOT = 'https://scholar.google.it'
    SCHOLAR = 'scholar'
    LANGUAGE = 'en'
    QUERY = 'apache spark'

    params = {'hl': LANGUAGE,
              'q': urllib.quote_plus(QUERY)}

    web_query = WEB_ROOT + '/' + SCHOLAR + '?' + urllib.urlencode(params)

    # request = urllib2.Request(web_query, None, headers)
    explore_google_pages(web_query, pages=5)