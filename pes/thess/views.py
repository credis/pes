# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext_lazy as _
from pes_local.models import Concept, Scheme
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404



def detailConcept(request, c_id):
    try:
        concept = Concept.objects.get(id=c_id)
    except Concept.DoesNotExist:
        raise Http404
    return render_to_response('concept/detail.html', {'concept': concept}, context_instance=RequestContext(request))


def detailScheme(request, c_id):
    try:
        scheme = Scheme.objects.get(id=c_id)
    except Scheme.DoesNotExist:
        raise Http404
    return render_to_response('scheme/detail.html', {'scheme': scheme}, context_instance=RequestContext(request))
