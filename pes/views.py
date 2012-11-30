# -*- coding:utf-8 -*-
# Create your views here.
from django.utils.translation import ugettext_lazy as _
# from pes.org.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from haystack.query import SearchQuerySet
from djrdf.import_rdf.models import SparqlQuery
from pes_local.models import Exchange, Organization, Article
from django.conf import settings
import json
from django.contrib.sites.models import Site
import urllib
from haystack.views import FacetedSearchView
from djrdf.tools import uri_to_json
from django.core.paginator import Paginator, InvalidPage



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
# def index(request):
#     context = {}
#     context['intro'] = u"%s" % Site.objects.get_current().name
#     sqom = SparqlQuery.objects.get(label='ordered by modified')
#     sq = sqom.query % str(Exchange.rdf_type)
#     res = Exchange.db.query(sq, initNs=settings.NS)
#     # form = MyFacetedSearchForm()
#     first10 = _first(res, 10, Exchange)
#     context['last_annonces'] = first10
#     sqoc = SparqlQuery.objects.get(label='ordered by created')
#     context['last_articles'] = _first(Article.db.query(sqoc.query % str(Article.rdf_type), initNs=settings.NS), 10, Article)

#     exchanges = []
#     for e in first10:
#         gj = e.to_geoJson()
#         if gj:
#             exchanges.append(gj)

#     exchanges = {"type": "FeatureCollection", "features":  exchanges}
#     context['geoJson'] = json.dumps(exchanges)

#     # Un beau moyen de faire des variables globales....
#     setattr(settings, 'PES_REMOTE_CLIENT', request.META.get('REMOTE_ADDR', None))

#     return render_to_response('home.html', context, RequestContext(request))


import logging
log = logging.getLogger('pes')


def get_rdf(request):
    uri = request.GET.get('url', '')
    return HttpResponse(uri_to_json(uri), mimetype="application/json")


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


def suggestions(request):
    model = request.GET['model_name']
    term = request.GET['q']
    limit = request.GET['limit']
    search_field = '%s_label' % model
    query_args = {search_field: term}
    qs = SearchQuerySet().autocomplete(**query_args).values(search_field, "uri")
    html = u''
    for r in qs:
        html += r[search_field] + u'|' + r["uri"] + u'\n'
    return HttpResponse(html)




# # Auto complete features... to be used with JQuery or ...
# def suggestion(request):
#     word = request.GET['q']
#     limit = request.GET['limit']

#     results = SearchQuerySet().autocomplete(content_auto=word)
#     if limit:
#     results = results[:int(limit)]
#     # Ici il y a un peu plus de boulot.... Il faut revenir aux mots
#     # les tags sont des groupes de mots
#     resp = "\n".join([r.object.name for r in results])
#     return HttpResponse(resp)


def SentryHandler500(request):
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html')  # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
        'STATIC_URL': settings.STATIC_URL,
    })))





class JsonFacetedSearchView(FacetedSearchView):

    def __name__(self):
        return "JsonFacetedSearchView"

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }

        if self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())
        return render_to_response(self.template, \
                                  context, \
                                  context_instance=self.context_class(self.request), \
                                  mimetype="application/json")


    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 0:
            raise Http404("Pages should be 0 or greater.")

        # Suppress pagination by creating a single page with all results
        if page_no == 0:
            paginator = Paginator(self.results, self.results.count())
            return (paginator, paginator.page(1))
        else:
            return super(JsonFacetedSearchView, self).build_page()



class ImportJsonFacetedSearchView(JsonFacetedSearchView):
    def __name__(self):
        return "ImportJsonFacetedSearchView"

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}

        # This way the form can always receive a list containing zero or more
        # facet expressions:
        form_kwargs['models'] = self.request.GET.getlist("model")

        return super(ImportJsonFacetedSearchView, self).build_form(form_kwargs)



class HomeSearchView(FacetedSearchView):

    def __name__(self):
        return "HomeSearchView"

    def extra_context(self):
        context = super(HomeSearchView, self).extra_context()
        context['intro'] = u"%s" % Site.objects.get_current().name

        sqom = SparqlQuery.objects.get(label='ordered by modified')
        sq = sqom.query % str(Exchange.rdf_type)

        res = Exchange.db.query(sq, initNs=settings.NS)
        first10 = _first(res, 10, Exchange)
        context['last_annonces'] = first10       

        org_sq = sqom.query % str(Organization.rdf_type)
        org_res = Organization.db.query(org_sq, initNs=settings.NS)
        org_10 = _first(org_res, 10, Organization)
        context['last_org'] = org_10

        sqoc = SparqlQuery.objects.get(label='ordered by created')
        context['last_articles'] = _first(Article.db.query(sqoc.query % str(Article.rdf_type), initNs=settings.NS), 10, Article)
        return context

