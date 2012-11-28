# -*- coding:utf-8 -*-
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.db import models
from rdfalchemy import rdfSingle, rdfMultiple
from django.conf import settings
from djrdf.models import myRdfSubject, djRdf
from pes.utils import loc_to_point
import rdflib


class Event(djRdf, myRdfSubject):
    # rdf attributes
    # rdf_type = settings.NS.vcal.Vevent   #  move to the pes_local class
    title = rdfSingle(settings.NS.vcal.summary)
    content = rdfSingle(settings.NS.vcal.description)
    person = rdfSingle(settings.NS.vcal.contact, range_type=settings.NS.person.Person)
    organization = rdfSingle(settings.NS.vcal.organizer, range_type=settings.NS.org.Organization)
    location = rdfMultiple(settings.NS.locn.location, range_type=settings.NS.dct.Location)
    startdate = rdfSingle(settings.NS.vcal.dtstart)
    tags = rdfMultiple(settings.NS.dct.subject, range_type=settings.NS.skosxl.Label)

    class Meta:

        abstract = True
        verbose_name = _(u'Event')
        verbose_name_plural = _(u'Events')

    @property
    def label(self):
        return self.title


    @models.permalink
    def get_absolute_url(self):
        return ('pes.agenda.views.detailEvent', [str(self.id)])


    @property
    def geo_point(self):
        if self.location and len(self.location) > 0:
            return  loc_to_point(self.location[0])
        elif self.organization:
            return self.organization.geo_point

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

