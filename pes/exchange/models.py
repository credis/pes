# -*- coding:utf-8 -*-
# Create your models here.
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rdfalchemy import rdfMultiple, rdfSingle
from djrdf.models import myRdfSubject, djRdf
from django.conf import settings
from rdfalchemy.orm import mapper
from pes.utils import fromAddrToPoint
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
    location = rdfMultiple(settings.NS.locn.location, range_type=settings.NS.locn.Address)

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
    def geoPoint(self):
        addr = None
        if len(self.location) > 0:
            addr = self.location[0]
        # on peut forcer et utiliser la localization de lù'arganization
        if not addr:
            return self.publisher.geoPoint
        else:
            return fromAddrToPoint(addr)


    @models.permalink
    def get_absolute_url(self):
        return ('pes.exchange.views.detailExchange', [str(self.id)])

    def to_geoJson(self):
        if self.geoPoint:
            return {
               "type": "Feature",
                "properties": {
                        "name": self.title.encode('utf-8'),
                        "popupContent": "<h4>" + self.title.encode('utf-8') + "</h4><p><a href='" + self.get_absolute_url() + "'>" + self.title.encode('utf-8') + "</a></p>"
                        },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [self.geoPoint.x, self.geoPoint.y]
                        }
                    }



    def proposition(self):
        query = SparqlQuery.objects.get(label='possible exchange').query % (self.uri, self.uri, self.uri)
        res = map(lambda x: x[0], self.db.query(query, initNs=settings.NS))
        return map(self.__class__, res)


