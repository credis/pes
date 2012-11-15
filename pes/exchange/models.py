# -*- coding:utf-8 -*-
# Create your models here.
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rdfalchemy import rdfMultiple, rdfSingle
from djrdf.models import myRdfSubject, djRdf
from django.conf import settings
from rdfalchemy.orm import mapper
from pes.utils import loc_to_point
from djrdf.import_rdf.models import SparqlQuery


class Exchange(djRdf, myRdfSubject):
    # rdf_type = settings.NS.ess.Exchange
    label = rdfSingle(settings.NS.rdfs.label)
    title = rdfSingle(settings.NS.dct.title)
    description = rdfSingle(settings.NS.dct.description)
    tags = rdfMultiple(settings.NS.dct.subject, range_type=settings.NS.skosxl.Label)
    category = rdfSingle(settings.NS.ov.category)
    publisher = rdfSingle(settings.NS.dct.publisher, range_type=settings.NS.org.Organization)
    area = rdfMultiple(settings.NS.gr.eligibleRegions, range_type=settings.NS.dct.location)
    method = rdfSingle(settings.NS.ess.hasMethod)
    location = rdfMultiple(settings.NS.locn.location, range_type=settings.NS.dct.Location)

    class Meta:
        abstract = True

    @property
    def offered_by(self):
        org = mapper()[str(settings.NS.org.Organization)]
        return map(org, list(self.db.subjects(settings.NS.gr.offers, self)))

    @property
    def seeked_by(self):
        org = mapper()[str(settings.NS.org.Organization)]
        return map(org, list(self.db.subjects(settings.NS.gr.seeks, self)))

    @property
    def geo_point(self):
        if self.location and len(self.location) > 0:
            return  loc_to_point(self.location[0])
        elif self.publisher:
            return self.publisher.geo_point

    def to_geoJson(self):
        if self.geo_point:
            return {
               "type": "Feature",
                "properties": {
                        "name": self.title.encode('utf-8'),
                        "popupContent": "<h4>" + self.title.encode('utf-8') + "</h4><p><a href='" + self.get_absolute_url() + "'>" + self.title.encode('utf-8') + "</a></p>"
                        },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [self.geo_point.x, self.geo_point.y]
                        }
                    }


    @models.permalink
    def get_absolute_url(self):
        return ('pes.exchange.views.detailExchange', [str(self.id)])

    def proposition(self):
        if self.publisher:
            if self in self.publisher.offers:
                query = SparqlQuery.objects.get(label='possible exchange offer').query % (self.uri, self.uri, self.uri)
            elif self in self.publisher.seeks:
                query = SparqlQuery.objects.get(label='possible exchange seek').query % (self.uri, self.uri, self.uri)
            else:
                query = None
            if query:
                res = map(lambda x: x[0], self.db.query(query, initNs=settings.NS))
                return map(self.__class__, res)
        return []





class Product(djRdf, myRdfSubject):    # rdf attributes
    # rdf_type = settings.NS.skosxl.Label   #  move to the pes_local class
    title = rdfSingle(settings.NS.schema.name)
    description = rdfSingle(settings.NS.schema.description)
    organization = rdfSingle(settings.NS.schema.manufacturer)
    tags = rdfMultiple(settings.NS.dct.subject, range_type=settings.NS.skosxl.Label)

    class Meta:

        abstract = True
        verbose_name = _(u'Product')
        verbose_name_plural = _(u'Products')

    @models.permalink
    def get_absolute_url(self):
        return ('pes.product.views.detailProduct', [str(self.id)])
