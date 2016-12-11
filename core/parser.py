class Parser:

    def __init__(self):
        pass

    def parse(self, page):
        records = page.find_all('div', {'class': 'gs_r'})
        for record in records:
            self._parse_scholar_record(record)

    def _parse_scholar_record(self, record):
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