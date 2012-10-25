# -*- coding:utf-8 -*-
from django.conf import settings
from rdfalchemy.orm import mapper
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point



def validGeoPoint(p):
    return (-90 <= p.y <= 90) and (-180 <= p.x <= 180)



def fromAddrToPoint(addr):
    if not addr:
        return None
    Loc = mapper()[str(settings.NS.dct.Location)]
    loc = map(Loc, list(addr.db.subjects(settings.NS.locn.address, addr)))
    if len(loc) > 0:
        loc = loc[0]
    else:
        return None

    if loc.geometry and loc.geometry.datatype == settings.NS.opens.wkt:
        geo = fromstr(str(loc.geometry))
        if isinstance(geo, Point) and validGeoPoint(geo):
            return geo


