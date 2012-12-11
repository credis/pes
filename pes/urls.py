from django.conf.urls import patterns, include, url
from pes.feeds import UpdateFeed, UpdateFeedObject
from django.views.generic import ListView
# from pes_local.models import  Tag, Exchange, Article, Product, Event, Person
from django.views.generic.base import TemplateView, RedirectView

from django.contrib import admin
admin.autodiscover()


handler500 = 'coop.views.SentryHandler500'

class TextPlainView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TextPlainView, self).render_to_response(
              context, content_type='text/plain', **kwargs)


from haystack.views import  search_view_factory
from pes.forms import PESFacetedSearchForm, ImportFacetedSearchForm
from pes.views import HomeSearchView


urlpatterns = patterns('',

    url(r'^', include('scanredirect.urls')),
    
    url(r'^$', search_view_factory(
        view_class=HomeSearchView,
        template='home.html',
        # searchqueryset=sqs,
        form_class=PESFacetedSearchForm,
        load_all=False
    ), name='haystack_search'),

    # Basic stuff
    url(r'^robots\.txt$', TextPlainView.as_view(template_name='robots.txt')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),

    # SubHub ans Atom Feeds
    url(r'^subscriber/', include('django_push.subscriber.urls')),
    url(r'^hub/', include('subhub.urls')),
    url(r'^feed/(?P<model>[\w-]+)/$', UpdateFeed()),
    url(r'^feed/(?P<model>[\w-]+)/(?P<obj>[A-Za-z0-9\-]+)/$', UpdateFeedObject()),


    # Json url
    url(r'^geojson/(?P<model>[\w-]+)/(?P<num>\d+)/$', 'pes.views.geojson'),
    url(r'^geojson/(?P<model>[\w-]+)/$', 'pes.views.geojson'),
    url(r'^get_rdf/$', 'pes.views.get_rdf'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^suggestions/$', 'pes.views.suggestions'),

    url(r'^org/$', ListView.as_view(model='pes_local.models.Organization', template_name="org/list.html", \
        paginate_by=30)),
    url(r'^org/(\d+)/$', 'pes.org.views.detailOrg'),

    url(r'^person/$', ListView.as_view(model='pes_local.models.Person', template_name="person/list.html", \
        paginate_by=30)),
    url(r'^person/(\d+)/$', 'pes.org.views.detailPerson'),

    url(r'^exchange/$', ListView.as_view(model='pes_local.models.Exchange', template_name="exchange/list.html",\
        paginate_by=30)),
    url(r'^exchange/(\d+)/$', 'pes.exchange.views.detailExchange'),

    url(r'^tag/$', ListView.as_view(model='pes_local.models.Tag', template_name="tag/list.html",\
        paginate_by=30)),
    url(r'^tag/(\d+)/$', 'pes.tag.views.detailTag'),

    url(r'^article/$', ListView.as_view(model='pes_local.models.Article', template_name="article/list.html",\
          paginate_by=30)),
    url(r'^article/(\d+)/$', 'pes.article.views.detailArticle'),

    url(r'^product/$', ListView.as_view(model='pes_local.models.Product', template_name="product/list.html",\
          paginate_by=30)),
    url(r'^product/(\d+)/$', 'pes.exchange.views.detailProduct'),
    

    url(r'^event/$', ListView.as_view(model='pes_local.models.Event', template_name="event/list.html",\
          paginate_by=30)),
    url(r'^event/(\d+)/$', 'pes.agenda.views.detailEvent'),

)





from pes.views import JsonFacetedSearchView, ImportJsonFacetedSearchView

urlpatterns += patterns('haystack.views',
    url(r'^searchJson/$', search_view_factory(
        view_class=JsonFacetedSearchView,
        template='search/resultat.json',
        form_class=PESFacetedSearchForm,
        load_all=False
    ), name='haystack_search'),
)


urlpatterns += patterns('haystack.views',
    url(r'^searchforimportJson/$', search_view_factory(
        view_class=ImportJsonFacetedSearchView,
        template='search/resultat.json',
        form_class=ImportFacetedSearchForm,
        # results_per_page=50,
        load_all=False
    ), name='haystack_search'),
)
