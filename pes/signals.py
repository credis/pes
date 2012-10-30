# from django_push.subscriber.signals import updated
from djrdf.import_rdf.models import EntrySite
from django.conf import settings
from rdflib import Graph, URIRef
import logging
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import urllib2
import urlparse

log = logging.getLogger('djrdf')



# TODO Utiliser managers filter ... et outils  Django
# c'est pas tres beau
# def fromUrlToEntry(url):
#     for eS in EntrySite.objects.all():
#         if url.startswith(eS.home):
#             return eS
#     return None




# Lets follows because the PES is not listerning on all
# types of objects
def follow(g, es):
    objs = list(g.objects(None, None))
    uriobjs = []
    for o in objs:
        if isinstance(o, URIRef):
            uriobjs.append(o)
    res = g
    validate = URLValidator(verify_exists=False)
    for o in uriobjs:
        if str(o).startswith(es.home) and not str(o).startswith(es.home + '/media'):
            try:
                validate(str(o))
                res += Graph().parse(str(o))
            except (ValidationError, urllib2.HTTPError):
                pass
    log.debug('end follow')
    return res



def listener(notification, **kwargs):
    ''' Process new content being provided from SuperFeedr
    '''
    log.debug("enter listener args %s" % kwargs)
    # retrieve the hub and thus the EntrySite
    hub, eS = None, None
    if 'links' in notification.feed:
        for link in notification.feed.links:
            if link.rel == 'hub':
                # Hub detected!
                hub = link.href
    try:
        if hub:
            eS = EntrySite.objects.get(hub=hub)
    except Exception, e:
        log.warning(u'%s' % e)

    log.debug("ok for Es %s and hub %s" % (eS, hub))
    validate = URLValidator(verify_exists=True)

    # log.debug("notification %s " % notification)
    for entry in notification.entries:
        # do something with entry here
        # entry.link donne le topic
        if eS:
            uri = str(entry.summary)
            up = urlparse.urlsplit(uri)
            url = up.scheme + '://' + up.netloc
            log.debug("Found an EntrySite %s and uri %s" % (eS, uri))
            try:
                validate(url)
                g = Graph()
                g.parse(uri)
                log.debug('uri parse')
                # g = follow(g, eS)
                log.debug('follow ok')
                # log.debug("New graph parsed %s " % g.serialyse(format='n3'))
                eS.toSesameRep(settings.SESAME_REPOSITORY_NAME, g, None, None)
                log.debug("Graph updated in SEsame")
            except ValidationError:
                pass

        


