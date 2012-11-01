from django.conf.urls import patterns, include, url
from pes.feeds import UpdateFeed, UpdateFeedObject
from django.views.generic import ListView
from pes_local.models import Organization, Tag, Exchange, Article

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pes.views.index'),

    url(r'^subscriber/', include('django_push.subscriber.urls')),
    url(r'^hub/', include('subhub.urls')),
    url(r'^feed/(?P<model>[\w-]+)/$', UpdateFeed()),
    url(r'^feed/(?P<model>[\w-]+)/(?P<obj>[A-Za-z0-9\-]+)/$', UpdateFeedObject()),


    url(r'^geojson/((?P<model>[\w-]+))/(?P<num>\d+)/$', 'pes.views.geojson'),
    url(r'^geojson/((?P<model>[\w-]+))/$', 'pes.views.geojson'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    url(r'^org/$', ListView.as_view(model=Organization, template_name="org/list.html")),
    url(r'^org/(\d+)/$', 'pes.org.views.detailOrg'),
    url(r'^exchange/$', ListView.as_view(model=Exchange, template_name="exchange/list.html")),
    url(r'^exchange/(\d+)/$', 'pes.exchange.views.detailExchange'),
    url(r'^tag/$', ListView.as_view(model=Tag, template_name="tag/list.html")),
    url(r'^tag/(\d+)/$', 'pes.tag.views.detailTag'),
    url(r'^article/$', ListView.as_view(model=Article, template_name="article/list.html",\
          paginate_by=30)),
    url(r'^article/(\d+)/$', 'pes.article.views.detailArticle'),

)




from haystack.views import  search_view_factory, FacetedSearchView
from pes.forms import MyFacetedSearchForm

urlpatterns += patterns('haystack.views',
    url(r'^search/$', search_view_factory(
        view_class=FacetedSearchView,
        template='search/search.html',
        # searchqueryset=sqs,
        form_class=MyFacetedSearchForm
    ), name='haystack_search'),
)