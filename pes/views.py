# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext_lazy as _
# from pes.org.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from django.template import RequestContext
from djrdf.import_rdf.models import SparqlQuery
from pes_local.models import Exchange, Organization
from django.conf import settings
import json


def _first(gen, size, cls):
    res = []
    for i in range(size):
        res.append(cls(gen.next()[0]))
    return res






# Should use a template....
def index(request):
    context = {}
    context['intro'] = u""" %s Welcome """ % settings.PROJECT_NAME.upper()
    sq = SparqlQuery.objects.get(label='ordered by modified')
    sq = sq.query % str(Exchange.rdf_type)
    res = Exchange.db.query(sq,  initNs=settings.NS)
    first10 = _first(res, 10, Exchange)
    context['dernieres_annonces'] = first10

    exchanges = []
    for e in first10:
        gj = e.to_geoJson()
        if gj:
            exchanges.append(gj)

    exchanges = {"type": "FeatureCollection", "features":  exchanges}
    context['geoJson'] = json.dumps(exchanges)

    return render_to_response('home.html', context, RequestContext(request))



def geojson(request, model, num):
    if model == 'exchange':
        cls = Exchange
    elif model == 'organization':
        cls = Organization

    if cls:
        sq = SparqlQuery.objects.get(label='ordered by modified')
        sq = sq.query % str(cls.rdf_type)
        res = cls.db.query(sq,  initNs=settings.NS)
        first = _first(res, int(num), cls)

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
