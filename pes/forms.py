# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from haystack.forms import SearchForm, HighlightedSearchForm, FacetedSearchForm
from haystack.utils.geo import Point, D
from django.contrib.gis.utils import GeoIP

from pes.tag.forms import TagForm as BaseTagForm
from pes_local.models import Organization, Exchange
from django.conf import settings





# Le code si dessous ne sert pas
class MySearchForm(HighlightedSearchForm):
    marseille = Point(5.3697800, 43.2964820)


    latitude = forms.DecimalField(required=False)
    longitude = forms.DecimalField(required=False)
    dist = forms.IntegerField(required=False, label=_(u'Distance max'))

    def search(self):
        # First, store the SearchQuerySet received from other processing
        sqs = super(MySearchForm, self).search()
        if self.is_bound:
            if self.cleaned_data['latitude'] and self.cleaned_data['longitude']:
                point = Point(self.cleaned_data['latitude'], 
                                self.cleaned_data['longitude'])
            else:
                point = self.marseille
            if self.cleaned_data['dist']:
                max_dist = D(km=self.cleaned_data['dist'])
                sqs = sqs.dwithin('location', point, max_dist).distance('location', point).order_by('distance')

        return sqs


class MyFacetedSearchForm(FacetedSearchForm):
    # latitude = forms.DecimalField(required=False)
    # longitude = forms.DecimalField(required=False)
    dist = forms.IntegerField(required=False, label=_(u'Distance max'))
    marseille = Point(5.3697800, 43.2964820)

    _sqs_cache = None

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(MyFacetedSearchForm, self).search()
        sqs = sqs.facet('zone').facet('category')#.facet('modified')

        ip = getattr(settings, 'PES_REMOTE_CLIENT', None)
        g = GeoIP(path=settings.PROJECT_PATH + '/config/GEO/')

        if ip and g.city(ip):
            point = Point(g.city(ip)['longitude'], g.city(ip)['latitude'])
        else:
            point = self.marseille  # default city



        if self.is_bound:
            # sqs = sqs.autocomplete(content_auto=self.cleaned_data['q'])

            # if self.cleaned_data['latitude'] and self.cleaned_data['longitude']:
            #     print 'latitude %s type lat %s' % (self.cleaned_data['latitude'], type(self.cleaned_data['latitude']))
            #     point = Point(self.cleaned_data['latitude'], 
            #                   self.cleaned_data['longitude'])
            # else:
            #     point = self.marseille

            if self.cleaned_data['dist']:
                max_dist = D(km=self.cleaned_data['dist'])
                # Une petite idee qui ne marche pas.... ca casse le type searchquery
                # good_distance = lambda x: distance(point, x.object.geoPoint, max_dist)
                # sqs = filter(good_distance, sqs)
                sqs = sqs.dwithin('location', point, max_dist).distance('location', point).order_by('distance')


        self._sqs_cache = sqs
        return sqs

    def geoJson(self):
        if not self._sqs_cache:
            self.search()
        result = []
        for s in self._sqs_cache:
            if s.model == Organization or s.model == Exchange:
                gj = s.object.to_geoJson()
                if gj:
                    result.append(gj)
        result = {"type": "FeatureCollection", "features":  result}
        return result








# calculer des distances
# import geopy
# geopy.distance.distance = geopy.distance.GreatCircleDistance
# d = geopy.distance.distance(point1, point2).km

import geopy
geopy.distance.distance = geopy.distance.GreatCircleDistance


def distance(p1, p2, dist):
    if p2:
        return geopy.distance.distance(p1, p2).km <= dist
    return True
