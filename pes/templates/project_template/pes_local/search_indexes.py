# -*- coding:utf-8 -*-
from haystack import indexes
from pes.search_indexes import OrganizationIndex as BaseOrganizationIndex
from pes.search_indexes import ExchangeIndex as BaseExchangeIndex
from pes.search_indexes import ArticleIndex as BaseArticleIndex
from pes.search_indexes import WordIndex as BaseWordIndex



# If you dont want to use the default index, please comment the following
# lines and write your own indexes

class OrganizationIndex(BaseOrganizationIndex, indexes.Indexable):
    pass


class ExchangeIndex(BaseExchangeIndex, indexes.Indexable):
    pass


class ArticleIndex(BaseArticleIndex, indexes.Indexable):
    pass


class WordIndex(BaseWordIndex, indexes.Indexable):
    pass
