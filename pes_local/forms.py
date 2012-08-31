# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from haystack.forms import SearchForm, HighlightedSearchForm, FacetedSearchForm
from haystack.utils.geo import Point, D
from pes.tag.forms import TagForm as BaseTagForm




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
    latitude = forms.DecimalField(required=False)
    longitude = forms.DecimalField(required=False)
    dist = forms.IntegerField(required=False, label=_(u'Distance max'))
    marseille = Point(5.3697800, 43.2964820)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(MyFacetedSearchForm, self).search()
        sqs = sqs.facet('zone').facet('category').facet('modified')

        if self.is_bound:
            # sqs = sqs.autocomplete(content_auto=self.cleaned_data['q'])

            if self.cleaned_data['latitude'] and self.cleaned_data['longitude']:
                print 'latitude %s type lat %s' % (self.cleaned_data['latitude'], type(self.cleaned_data['latitude']))
                point = Point(self.cleaned_data['latitude'], 
                              self.cleaned_data['longitude'])
            else:
                point = self.marseille

            if self.cleaned_data['dist']:
                max_dist = D(km=self.cleaned_data['dist'])
                sqs = sqs.dwithin('location', point, max_dist).distance('location', point).order_by('distance')

        return sqs
