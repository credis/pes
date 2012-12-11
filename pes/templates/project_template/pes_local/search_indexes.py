# -*- coding:utf-8 -*-
from haystack import indexes
from pes.search_indexes import OrganizationIndex as BaseOrganizationIndex
from pes.search_indexes import ExchangeIndex as BaseExchangeIndex
from pes.search_indexes import ProductIndex as BaseProductIndex
from pes.search_indexes import ArticleIndex as BaseArticleIndex
from pes.search_indexes import WordIndex as BaseWordIndex
from pes.search_indexes import PersonIndex as BasePersonIndex
from pes.search_indexes import ContactIndex as BaseContactIndex
from pes.search_indexes import LocationIndex as BaseLocationIndex
from pes.search_indexes import EventIndex as BaseEventIndex
from pes_local.models import Organization, Person, Exchange
from pes_local.models import Event, Article, Product, Location, Contact


# If you dont want to use the default index, please comment the following
# lines and write your own indexes


class EventIndex(BaseEventIndex, indexes.Indexable):
    def get_model(self):
        return Event


class LocationIndex(BaseLocationIndex, indexes.Indexable):
    def get_model(self):
        return Location


class OrganizationIndex(BaseOrganizationIndex, indexes.Indexable):
    def get_model(self):
        return Organization


class ExchangeIndex(BaseExchangeIndex, indexes.Indexable):
    def get_model(self):
        return Exchange


class ProductIndex(BaseProductIndex, indexes.Indexable):
    def get_model(self):
        return Product


class ArticleIndex(BaseArticleIndex, indexes.Indexable):
    def get_model(self):
        return Article


class PersonIndex(BasePersonIndex, indexes.Indexable):
    def get_model(self):
        return Person

        
class ContactIndex(BaseContactIndex, indexes.Indexable):
    def get_model(self):
        return Contact





class WordIndex(BaseWordIndex, indexes.Indexable):
    pass



