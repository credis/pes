# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django import forms
from haystack.forms import FacetedSearchForm
from haystack.utils.geo import D
from pes.middleware import get_current_request
from pes.utils import get_geoIP, get_hostname




class PESFacetedSearchForm(FacetedSearchForm):
    # latitude = forms.DecimalField(required=False)
    # longitude = forms.DecimalField(required=False)
    dist = forms.IntegerField(required=False, label=_(u'Distance max'))

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(PESFacetedSearchForm, self).search()
        sqs = sqs.facet('zone').facet('category').facet('tags')  # .facet('modified')
        (point, city) = get_geoIP(get_current_request())
        self.fields['dist'].label = _(u'Distance max de %s' % city)

        if self.is_bound:
            if self.cleaned_data['dist']:
                max_dist = D(km=self.cleaned_data['dist'])
                sqs = sqs.dwithin('location', point, max_dist).distance('location', point).order_by('distance')

        return sqs




class ImportFacetedSearchForm(PESFacetedSearchForm):

    def __init__(self, *args, **kwargs):
        self.models = kwargs.pop("models", [])
        super(ImportFacetedSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(ImportFacetedSearchForm, self).search()
        m = map(lambda x: models.get_model('pes_local', x), self.models)

        # return only result not in the
        authority_home = get_hostname(get_current_request())
        sqs = sqs.exclude(uri__contains=authority_home)
        return sqs.models(*m)



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
