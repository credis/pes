from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^', include('pes.urls')),

)



from haystack.views import  search_view_factory, FacetedSearchView
from pes.forms import MyFacetedSearchForm

urlpatterns += patterns('haystack.views',
    url(r'^search/$', search_view_factory(
        view_class=FacetedSearchView,
        template='search/search.html',
        # searchqueryset=sqs,
        form_class=MyFacetedSearchForm,
        load_all = False
    ), name='haystack_search'),
)