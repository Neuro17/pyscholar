import urllib2
import urllib
from bs4 import BeautifulSoup
import pprint as pp

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) ' \
             'Gecko/2009021910 Firefox/3.0.7'

WEB_ROOT = 'https://scholar.google.it'
SCHOLAR = 'scholar'
LANGUAGE = 'en'
QUERY = 'mapreduce'

params = {'hl': LANGUAGE,
          'q': urllib.quote_plus(QUERY)}

headers = {'User-Agent': USER_AGENT}


def parse(params):
    return '&'.join(['{0}={1}'.format(k, v) for k, v in params.iteritems()])

web_query = WEB_ROOT + '/' + SCHOLAR + '?' + urllib.urlencode(params)

request = urllib2.Request(web_query, None, headers)

soup = BeautifulSoup(urllib2.urlopen(request).read(), "lxml")

records = soup.find_all('div', {'class': 'gs_r'})
print len(records)
for record in records[:1]:

    #--------------------------------------------------------------------------#
    #             article               |                  PDF                 #
    #                                   |                                      #
    #--------------------------------------------------------------------------#

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
