from article import Article
import logging

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
