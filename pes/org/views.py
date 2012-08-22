# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext_lazy as _
from pes_local.models import Organization
from pes.org.forms import OrgForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404



def detailOrg(request, org_id):
    try:
        org = Organization.objects.get(id=org_id)
    except Organization.DoesNotExist:
        raise Http404
    form = OrgForm().form(org)

    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        # As we have some select=multiple and rebind uses the .items() methode
        form.rebind(org, data=request.POST.lists())
        if form.validate():
            form.sync()
            # import pdb; pdb.set_trace()
            org.save()
            return render_to_response('org/detail.html', {'org': org, 'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('org/error.html', {'fields': form.errors.keys()})

    else:
        return render_to_response('org/detail.html', {'org': org, 'form': form}, context_instance=RequestContext(request))


