# -*- coding:utf-8 -*-

from djrdf.import_rdf.models import EntrySite
from django.conf import settings


# Here one can find method to initiate the aggreagator repository
# Cleanning the openRdf repository are not yet implemented.... use the 
# openrdf-workbench interface for this purpose



# if ctx == None, then every triples are stored without context
# if ctx == 'default', then the default context name for the endPoint is used

def allToSesameRep():
    for ed in EntrySite.objects.all():
        print """
    Importation of rdf data from %s
    """ % ed.label
    # Contexts seem to be useless
    ed.toSesameRep(settings.SESAME_REPOSITORY_NAME, ed.sparql(), None, None)

#


