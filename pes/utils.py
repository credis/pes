# -*- coding:utf-8 -*-
from django.conf import settings
from rdfalchemy.orm import mapper
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point
from djrdf.import_rdf.models import EntrySite
from django.conf import settings
from django.contrib.gis.utils import GeoIP
from django.contrib.gis.geos import Point
import socket
from djrdf.import_rdf.models import SparqlQuery


def first_items(gen, size, cls):
    res = []
    if size == None:
        try:
            while True:
                res.append(cls(gen.next()[0]))
        except StopIteration:
            pass
    else:
        try:
            for i in range(size):
                res.append(cls(gen.next()[0]))
        except Exception:
            pass
    return res


def get_ordererd_list(cls, number=None):
    sqom = SparqlQuery.objects.get(label='ordered by modified')
    sq = sqom.query % str(cls.rdf_type)
    res = cls.db.query(sq, initNs=settings.NS)
    if not number:
        return res
    else:
        return first_items(res, number, cls)



def validGeoPoint(p):
    return (-90 <= p.y <= 90) and (-180 <= p.x <= 180)


def get_geoIP(request):
    # marseille = Point(5.3697800, 43.2964820)
    clermont = Point(3.0870250, 45.7772220)
    ip = request.META.get('REMOTE_ADDR', None)

    g = GeoIP(path=settings.PROJECT_PATH + '/config/GEO/')

    if ip and g.city(ip):
        return (Point(g.city(ip)['longitude'], g.city(ip)['latitude']), 
               g.city(ip)['city'])
    else:
        return getattr(settings, 'DEFAULT_MAIN_CITY', (clermont, u'Clermont-Fd'))  # default city


def get_hostname(request):
    ip = request.META.get('REMOTE_ADDR', None)
    return socket.gethostbyaddr(ip)[0]


def map_coop_model(model):
    if model in settings.MAPPING_COOP_PES:
        return settings.MAPPING_COOP_PES[model]
    else:
        return model



def addr_to_point(addr):
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


def loc_to_point(loc):
    if loc.geometry and loc.geometry.datatype == settings.NS.opens.wkt:
        geo = fromstr(str(loc.geometry))
        if isinstance(geo, Point) and validGeoPoint(geo):
            return geo
    else:
        return None




# Here one can find 
# Cleanning the openRdf repository are not yet implemented.... use the 
# openrdf-workbench interface for this purpose



# if ctx == None, then every triples are stored without context
# if ctx == 'default', then the default context name for the endPoint is used

def allToSesameRep():
    """ method to initiate the aggreagator repository
    """
    for ed in EntrySite.objects.all():
        print """
    Importation of rdf data from %s
    """ % ed.label
    # Contexts seem to be useless
    ed.toSesameRep(settings.SESAME_REPOSITORY_NAME, ed.graph(), None, None, force=True)



def cleanallSesameRep():
    """ method to clean the aggreagator repository
    """
    for ed in EntrySite.objects.all():
        print """
    Clean all rdf data from %s
    """ % ed.label
    # Contexts seem to be useless
    ed.removeFromSesameRep(settings.SESAME_REPOSITORY_NAME,  None, None)


#: By default we'll set CORS Allow Origin * for all application/json responses
DEFAULT_CORS_PATHS = (
    ('/', ('application/json', ), (('Access-Control-Allow-Origin', '*'), )),
    ('/', ('text/html', ), (('Access-Control-Allow-Origin', '*'), )),
    ('/', ('application/xhtml', ), (('Access-Control-Allow-Origin', '*'), )),
)


class CORSMiddleware(object):
    """
Middleware that serves up representations with a CORS header to
allow third parties to use your web api from JavaScript without
requiring them to proxy it.

See: http://www.w3.org/TR/cors/

Installation
------------

1. Add to ``settings.MIDDLEWARE_CLASSES``::

'sugar.middleware.cors.CORSMiddleware',

2. Optionally, configure ``settings.CORS_PATHS`` if the default settings
aren't appropriate for your application. ``CORS_PATHS`` should be a
list of (path, content_types, headers) values where content_types and
headers are lists of mime types and (key, value) pairs, respectively.

Processing occurs first to last so you should order ``CORS_PATHS``
items from most to least specific.

See ``DEFAULT_CORS_PATHS`` for an example.

Notes
-----

* Although not officially a feature, the headers are not restricted to
the CORS spec and could conceivably include other values such as
desired (allowing, for example, custom ``Cache-Control`` settings).
"""

    def __init__(self):
        self.paths = getattr(settings, "CORS_PATHS", DEFAULT_CORS_PATHS)

    def process_response(self, request, response):
        content_type = response.get('content-type', '').split(";")[0].lower()

        for path, types, headers in self.paths:
            if request.path.startswith(path) and content_type in types:
                for k, v in headers:
                    response[k] = v
                break
        return response



