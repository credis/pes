# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext_lazy as _
from pes_local.models import Article
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404



def detailArticle(request, ex_id):
    try:
        art = Article.objects.get(id=ex_id)
    except Article.DoesNotExist:
        raise Http404

    else:
        return render_to_response('article/detail.html', {'article': art}, context_instance=RequestContext(request))



