# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext_lazy as _
from pes_local.models import Exchange, Product
from pes.exchange.forms import ExchangeForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404


def detailExchange(request, ex_id):
    try:
        ex = Exchange.objects.get(id=ex_id)
    except Exchange.DoesNotExist:
        raise Http404
    form = ExchangeForm().form(ex)

    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        # As we have some select=multiple and rebind uses the .items() methode
        form.rebind(ex, data=request.POST.lists())
        if form.validate():
            form.sync()
            # import pdb; pdb.set_trace()
            ex.save()
            return render_to_response('exchange/detail.html', {'ex': ex, 'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('exchange/error.html', {'fields': form.errors.keys()})

    else:
        return render_to_response('exchange/detail.html', {'ex': ex, 'form': form}, context_instance=RequestContext(request))



def detailProduct(request, pr_id):
    try:
        prod = Product.objects.get(id=pr_id)
    except Product.DoesNotExist:
        raise Http404

    else:
        return render_to_response('product/detail.html', {'product': prod}, context_instance=RequestContext(request))
