# -*- coding:utf-8 -*-
from django.conf import settings
from rdfalchemy.orm import mapper
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Point
from djrdf.import_rdf.models import EntrySite
from django.conf import settings



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
