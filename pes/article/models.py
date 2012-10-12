# -*- coding:utf-8 -*-
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from rdfalchemy import rdfSingle, rdfMultiple
from django.conf import settings
from djrdf.models import myRdfSubject, djRdf


class Article(djRdf, myRdfSubject):
    # rdf attributes
    # rdf_type = settings.NS.skosxl.Label   #  move to the pes_local class
    title = rdfSingle(settings.NS.dct.title)
    summary = rdfSingle(str(settings.NS['dct']) + 'abstract')
    content = rdfSingle(settings.NS.dct.description)
    person = rdfSingle(settings.NS.dct.creator)
    organization = rdfSingle(settings.NS.dct.publisher)

    tags = rdfMultiple(settings.NS.dct.subject, range_type=settings.NS.skosxl.Label)



