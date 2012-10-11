# -*- coding:utf-8 -*-
# Create your models here.
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rdfalchemy import rdfMultiple, rdfSingle
from djrdf.models import myRdfSubject, djRdf
from django.conf import settings
from rdfalchemy.orm import mapper


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

    @models.permalink
    def get_absolute_url(self):
        return ('pes.exchange.views.detailExchange', [str(self.id)])

