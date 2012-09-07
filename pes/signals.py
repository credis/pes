# from django_push.subscriber.signals import updated
from djrdf.import_rdf.models import EntrySite
from django.conf import settings
from rdflib import Graph
import logging

log = logging.getLogger('djrdf')



# TODO Utiliser managers filter ... et outils  Django
# c'est pas tres beau
# def fromUrlToEntry(url):
#     for eS in EntrySite.objects.all():
#         if url.startswith(eS.home):
#             return eS
#     return None



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


    print "ok for Es %s and hub %s" % (eS, hub)
    # log.debug("notification %s " % notification)
    for entry in notification.entries:
        # do something with entry here
        # entry.link donne le topic
        if eS:
            uri = str(entry.summary)
            log.debug("Found an EntrySite %s and uri %s" % (eS, uri))
            g = Graph()
            g.parse(uri)
            log.debug("New graph parsed %s " % g)
            eS.toSesameRep(settings.SESAME_REPOSITORY_NAME, g, None, None)


