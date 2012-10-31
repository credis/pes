# -*- coding:utf-8 -*-
import datetime
from haystack import indexes
from pes.models import Word
from pes_local.models import Organization, Person, Exchange
from django.contrib.gis.geos import Point
from djrdf.import_rdf.models import SparqlQuery
from django.conf import settings
from rdfalchemy.orm import mapper

# TODO : We have to decide if theses data have to be store
# in openrdf store or not.
import rdflib
ess_data = rdflib.Graph()
ess_data.parse(settings.PROJECT_PATH + '/config/rdf/exchange-methods.ttl', format='n3')


if getattr(settings, 'HAYSTACK_REALTIME', False):
    Indexes = indexes.RealTimeSearchIndex
else:
    Indexes = indexes.SearchIndex



# A rajouter enventuellement pour simplifier un peu la tache de backend
# import re


# def remove_html_tags(data):
#     p = re.compile(r'<.*?>')
#     return p.sub('', data)


# The main class
class PESIndex(Indexes):
    text = indexes.CharField(document=True, use_template=True)
    tags = indexes.MultiValueField(boost=1.2)
    category = indexes.MultiValueField(faceted=True)
    modified = indexes.DateField(model_attr='dct_modified', faceted=True)
    zone = indexes.MultiValueField(faceted=True)
    # suggestions = indexes.CharField(faceted=True)  # for solr only?
    location = indexes.LocationField()

    # def prepare_modified(self, obj):
    #     return [str(obj.modified)]

    # Ok this is very 'lourding' but... with the ClassInstances method we 
    # avoid many problems.... such as relocation of uri 
    # the cost is to double the request ...
    def index_queryset(self):
        "Used when the entire index for model is updated."
        list_of_ids = map(lambda x: x.id, list(self.get_model().ClassInstances()))
        return self.get_model().objects.filter(pk__in=list_of_ids)

    def prepare_tags(self, obj):
        return ["%s " % tag.name for tag in obj.tags]

    # Comme on s'en sert de facette. On n'a pas besoin de trop de details
    def prepare_modified(sel, obj):
        return obj.dct_modified.date()

    def prepare_zone(self, obj):
        # On traite pour le moment les zones contenantes
        query = SparqlQuery.objects.get(label='geo contains')
        return map(lambda x: x[0].toPython(), set(obj.db.query(query.query % obj.uri, initNs=settings.NS)))

    def prepare(self, obj):
        # print "prepare %s" % obj
        prepared_data = super(PESIndex, self).prepare(obj)
        prepared_data['text'] = prepared_data['text'] + ' ' + ' '.join(prepared_data['tags']) + \
              ' ' + ' '.join(prepared_data['category'])
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data







class OrganizationIndex(PESIndex, indexes.Indexable):
    exchange = indexes.MultiValueField()

    def get_model(self):
        return Organization


    def prepare_category(self, obj):
        return [u"association"]

    def prepare_exchange(self, obj):
        title = lambda x: x.title
        return map(title, obj.seeks) + map(title, obj.offers)

    def prepare_location(self, obj):
        res = obj.geoPoint
        if res == None:
            res = Point(x=0, y=0)
        return "%s,%s" % (res.y, res.x)

    def prepare(self, obj):
        # print "prepare %s" % obj
        prepared_data = super(OrganizationIndex, self).prepare(obj)
        prepared_data['text'] = prepared_data['text'] + ' ' + ' '.join(prepared_data['exchange'])
        return prepared_data





class ExchangeIndex(PESIndex, indexes.Indexable):
    method = indexes.MultiValueField()

    def get_model(self):
        return Exchange

    def prepare_method(self, obj):
        if obj.method:
            query = SparqlQuery.objects.get(label='fr filter').query % str(obj.method.n3())
            return map(lambda x: x[0].toPython(), ess_data.query(query))
        else:
            return []

    def prepare_category(self, obj):
        return [u"annonce"]

    def prepare_location(self, obj):
        res = obj.geoPoint
        if res == None:
            res = Point(x=0, y=0)
        return "%s,%s" % (res.y, res.x)


    def prepare(self, obj):
        # print "prepare %s" % obj
        prepared_data = super(ExchangeIndex, self).prepare(obj)
        prepared_data['text'] = prepared_data['text'] + ' ' + ' '.join(prepared_data['method'])
        return prepared_data






# On se sert de la liste des tags pour faire de l'autocomplite
# class TagIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     content_auto = indexes.EdgeNgramField(model_attr='label')

#     def get_model(self):
#         return Tag

#     def index_queryset(self):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.filter(modified__lte=datetime.datetime.now())


# On cree les instance de Word. Cette methode doit etre appeller




class WordIndex(Indexes, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Word

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


# Bof bof, va-t-on ou pas indexer les personnes?
class PersonIndex(PESIndex):
    text = indexes.CharField(document=True, use_template=True)
    # Define the additional field.
    # rendered = indexes.CharField(use_template=True, indexed=False)
    suggestions = indexes.CharField()

    def get_model(self):
        return Person


    def prepare(self, obj):
        prepared_data = super(PersonIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(modified__lte=datetime.datetime.now())


