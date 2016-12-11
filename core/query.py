import utils
from urllib import urlencode


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

    def _quote(self):
        for attr in [a for a in vars(q) if not a.startswith('_')]:
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
                       'as_vis': self.citations}
        return utils.SCHOLAR_SITE + '/scholar?' + urlencode(self._query)

if __name__ == '__main__':
    q = Query(authors=['page', 'brin'], words=['pagerank'],
              phrase='bringing order to the web')
    print q.build()