from django.conf.urls import patterns, include, url
from pes.feeds import UpdateFeed, UpdateFeedObject
from django.views.generic import ListView
from pes_local.models import Organization, Tag, Exchange, Article, Product, Event, Person

from django.contrib import admin
admin.autodiscover()


handler500 = 'coop.views.SentryHandler500'


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




    # SubHub ans Atom Feeds
    url(r'^subscriber/', include('django_push.subscriber.urls')),
    url(r'^hub/', include('subhub.urls')),
    url(r'^feed/(?P<model>[\w-]+)/$', UpdateFeed()),
    url(r'^feed/(?P<model>[\w-]+)/(?P<obj>[A-Za-z0-9\-]+)/$', UpdateFeedObject()),


    # Json url
    url(r'^geojson/((?P<model>[\w-]+))/(?P<num>\d+)/$', 'pes.views.geojson'),
    url(r'^geojson/((?P<model>[\w-]+))/$', 'pes.views.geojson'),
    url(r'^get_rdf/((?P<uri>[\S]+))/$', 'pes.views.get_rdf'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^suggestions/$', 'pes.views.suggestions'),

    url(r'^org/$', ListView.as_view(model=Organization, template_name="org/list.html", \
        paginate_by=30)),
    url(r'^org/(\d+)/$', 'pes.org.views.detailOrg'),

    url(r'^person/$', ListView.as_view(model=Person, template_name="person/list.html", \
        paginate_by=30)),
    url(r'^person/(\d+)/$', 'pes.org.views.detailPerson'),

    url(r'^exchange/$', ListView.as_view(model=Exchange, template_name="exchange/list.html",\
        paginate_by=30)),
    url(r'^exchange/(\d+)/$', 'pes.exchange.views.detailExchange'),

    url(r'^tag/$', ListView.as_view(model=Tag, template_name="tag/list.html",\
        paginate_by=30)),
    url(r'^tag/(\d+)/$', 'pes.tag.views.detailTag'),

    url(r'^article/$', ListView.as_view(model=Article, template_name="article/list.html",\
          paginate_by=30)),
    url(r'^article/(\d+)/$', 'pes.article.views.detailArticle'),

    url(r'^product/$', ListView.as_view(model=Product, template_name="product/list.html",\
          paginate_by=30)),
    url(r'^product/(\d+)/$', 'pes.article.views.detailProduct'),
    

    url(r'^event/$', ListView.as_view(model=Event, template_name="event/list.html",\
          paginate_by=30)),
    url(r'^event/(\d+)/$', 'pes.agenda.views.detailEvent'),

)





from pes.views import JsonFacetedSearchView

urlpatterns += patterns('haystack.views',
    url(r'^searchJson/$', search_view_factory(
        view_class=JsonFacetedSearchView,
        template='search/resultat.json',
        # searchqueryset=sqs,
        form_class=PESFacetedSearchForm,
        load_all=False
    ), name='haystack_search'),
)


urlpatterns += patterns('haystack.views',
    url(r'^searchforimportJson/$', search_view_factory(
        view_class=JsonFacetedSearchView,
        template='search/import.json',
        # searchqueryset=sqs,
        form_class=ImportFacetedSearchForm,
        load_all=False
    ), name='haystack_search'),
)
