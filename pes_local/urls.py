from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from pes_local.models import Organization, Tag, Exchange


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^', include('pes.urls')),
    url(r'^org/$', ListView.as_view(model=Organization, template_name="org/list.html")),
    url(r'^org/(\d+)/$', 'pes.org.views.detailOrg'),
    url(r'^exchange/$', ListView.as_view(model=Exchange, template_name="exchange/list.html")),
    url(r'^exchange/(\d+)/$', 'pes.exchange.views.detailExchange'),
    url(r'^tag/$', ListView.as_view(model=Tag, template_name="tag/list.html")),
    url(r'^tag/(\d+)/$', 'pes.tag.views.detailTag'),

)


from haystack.views import  search_view_factory, FacetedSearchView
from pes_local.forms import MyFacetedSearchForm

urlpatterns += patterns('haystack.views',
    url(r'^search/$', search_view_factory(
        view_class=FacetedSearchView,
        template='search/search.html',
        # searchqueryset=sqs,
        form_class=MyFacetedSearchForm
    ), name='haystack_search'),
)
