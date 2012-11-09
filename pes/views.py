# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext_lazy as _
# from pes.org.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from django.template import RequestContext
from djrdf.import_rdf.models import SparqlQuery
from pes_local.models import Exchange, Organization, Article
from django.conf import settings
import json
from django.contrib.gis.utils import GeoIP
from django.contrib.gis.geos import Point
from django.contrib.sites.models import Site



def _first(gen, size, cls):
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






# Should use a template....
def index(request):
    context = {}
    context['intro'] = u"%s" % Site.objects.get_current().domain
    sqom = SparqlQuery.objects.get(label='ordered by modified')
    sq = sqom.query % str(Exchange.rdf_type)
    res = Exchange.db.query(sq, initNs=settings.NS)
    first10 = _first(res, 10, Exchange)
    context['last_annonces'] = first10
    sqoc = SparqlQuery.objects.get(label='ordered by created')
    context['last_articles'] = _first(Article.db.query(sqoc.query % str(Article.rdf_type), initNs=settings.NS), 10, Article)

    exchanges = []
    for e in first10:
        gj = e.to_geoJson()
        if gj:
            exchanges.append(gj)

    exchanges = {"type": "FeatureCollection", "features":  exchanges}
    context['geoJson'] = json.dumps(exchanges)

    # Un beau moyen de faire des variables globales....
    setattr(settings, 'PES_REMOTE_CLIENT', request.META.get('REMOTE_ADDR', None))

    return render_to_response('home.html', context, RequestContext(request))



def geojson(request, model, num=None):
    if model == 'exchange':
        cls = Exchange
    elif model == 'organization':
        cls = Organization

    if cls:
        sq = SparqlQuery.objects.get(label='ordered by modified')
        sq = sq.query % str(cls.rdf_type)
        res = cls.db.query(sq,  initNs=settings.NS)
        if num:
            first = _first(res, int(num), cls)
        else:
            first = _first(res, None, cls)

        result = []
        for e in first:
            gj = e.to_geoJson()
            if gj:
                result.append(gj)

    result = {"type": "FeatureCollection", "features":  result}
    return HttpResponse(json.dumps(result), mimetype="application/json")






# Auto complete features... to be used with JQuery or ...
def suggestion(request):
    word = request.GET['q']
    limit = request.GET['limit']

    results = SearchQuerySet().autocomplete(content_auto=word)
    if limit:
        results = results[:int(limit)]
    # Ici il y a un peu plus de boulot.... Il faut revenir aux mots
    # les tags sont des groupes de mots
    resp = "\n".join([r.object.name for r in results])
    return HttpResponse(resp)



def SentryHandler500(request):
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')  # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
        'STATIC_URL': settings.STATIC_URL,
    })))
