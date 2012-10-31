# -*- coding:utf-8 -*-
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.db import models
from rdfalchemy import rdfSingle, rdfMultiple
from django.conf import settings
from djrdf.models import myRdfSubject, djRdf
import rdflib


class Article(djRdf, myRdfSubject):
    # rdf attributes
    # rdf_type = settings.NS.skosxl.Label   #  move to the pes_local class
    title = rdfSingle(settings.NS.dct.title)
    summary = rdfSingle(rdflib.URIRef(str(settings.NS['dct']) + 'abstract'))
    content = rdfSingle(settings.NS.dct.description)
    person = rdfSingle(settings.NS.dct.creator)
    organization = rdfSingle(settings.NS.dct.publisher)

    tags = rdfMultiple(settings.NS.dct.subject, range_type=settings.NS.skosxl.Label)

    class Meta:

        abstract = True
        verbose_name = _(u'Article')
        verbose_name_plural = _(u'Articles')

    @models.permalink
    def get_absolute_url(self):
        return ('pes.article.views.detailArticle', [str(self.id)])

