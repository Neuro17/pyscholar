import datetime

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
