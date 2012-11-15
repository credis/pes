# -*- coding:utf-8 -*-
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from djrdf.models import myRdfSubject, djRdf
from rdfalchemy import rdfSingle
import string
from django.contrib.gis.geos import Point
import rdflib


# TODO il n'y a pas que des points ....MultiPolygon
def convert_wkt(pp):
    """
      Ok it is not vey nice to go from drting manipulation
      but until now I have no other solution
    """
    try:
        p = string.replace(str(pp), 'POINT(', '')
        p = string.replace(p, ')', '')
        p = p.split(' ')
        return Point(float(p[0]), float(p[1]))
    except Exception:
        return pp

rdflib.term.bind(settings.NS.opens.wkt, convert_wkt)



class Location(djRdf, myRdfSubject):
    # rdf_type = settings.NS.dct.Location
    geometry = rdfSingle(settings.NS.locn.geometry)
    address = rdfSingle(settings.NS.locn.address, range_type=settings.NS.locn.Address)

    class Meta:
        abstract = True

    @property
    def label(self):
        if self.address:
            return self.address.fullAddress
        return u''



class Address(myRdfSubject):
    rdf_type = settings.NS.locn.Address
    fullAddress = rdfSingle(settings.NS.locn.fullAddress)
    # geometry = rdfSingle(settings.NS.locn.geometry)


