# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext_lazy as _
from pes.org.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse
from haystack.query import SearchQuerySet


# Should use a template....
def index(request):
    context = {}
    context['intro'] = u""" %s Welcome """ % settings.PROJECT_NAME.upper()
    return render_to_response('home.html', context)



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
