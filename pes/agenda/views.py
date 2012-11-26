# Create your views here.
from django.utils.translation import ugettext_lazy as _
from pes_local.models import Event
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404



def detailEvent(request, ex_id):
    try:
        evt = Event.objects.get(id=ex_id)
    except Event.DoesNotExist:
        raise Http404

    else:
        return render_to_response('event/detail.html', {'event': evt}, context_instance=RequestContext(request))
