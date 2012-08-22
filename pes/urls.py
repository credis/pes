from django.conf.urls import patterns, include, url
from pes.feeds import UpdateFeed, UpdateFeedObject



urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pes.views.index'),

    url(r'^subscriber/', include('django_push.subscriber.urls')),
    url(r'^hub/', include('subhub.urls')),
    url(r'^feed/(?P<model>[\w-]+)/$', UpdateFeed()),
    url(r'^feed/(?P<model>[\w-]+)/(?P<obj>\w+)/$', UpdateFeedObject()),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # haystack
    # (r'^search/', include('haystack.urls')),



    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


