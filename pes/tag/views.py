# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext_lazy as _
from pes_local.models import Tag
from pes.tag.forms import *
from django.shortcuts import render_to_response
from django.http import Http404


def detailTag(request, tag_id):
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        raise Http404
    form = TagForm().form(tag)
    # return HttpResponse("Hello, world. You're at the PES Tag detail %s." % tag.label)
    return render_to_response('tag/detail.html', {'tag': tag, 'form': form})
