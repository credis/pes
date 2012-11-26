# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django_push.publisher.feeds import Feed
#from django.contrib.syndication.views import Feed
from django.db.models.loading import get_model
from django.contrib.contenttypes.models import ContentType
from urlparse import urlsplit
import pes
from django.db import models
from pes.utils import map_coop_model




class UpdateFeed(Feed):
    title = _(u"Updates for %s." % Site.objects.get_current().name)
    link = "/feed/" 
    description = _(u"All records updates listed on the %s website." % Site.objects.get_current().name)
    hub = "http://%s/hub/" % Site.objects.get_current()



    def items(self):
        # Use ContenType to find the models .... If possible
        # ping dans save de model uri
        # TODO suppress the modified field and use sparql query to build
        # the selected items
        return get_model(self._mType.app_label, self._model).objects.order_by('-modified')[:5]
        # if not isinstance(self._mType, list):
        #     return get_model(self._mType.app_label, self._model).objects.order_by('-modified')[:5]
        # else:
        #     # self._mType should contains class
        #     res = []
        #     for t in self._mType:
        #         res.extend(t.objects.order_by('-modified')[:5])
        #     res = sorted(res, key=lambda x: x.modified)
        #     return res[:5]


    # to deal with overwriting ...
    def item_title(self, item):
        try:
            return item.label()
        except:
            return item.label

    def item_guid(self, item):
        scheme, host, path, query, fragment = urlsplit(item.uri)
        # path has the follong pathern : '/id/<class_name>/<uuid>/', so sp[3] is the uuid
        sp = path.split('/')
        try:
            return "%s_%s" % (sp[3], item.modified)
        except:
            return "%s_%s" % (path, item.modified)


    def item_description(self, item):
        return item.uri

    def item_link(self, item):
        return item.uri

    # def item_extra_kwargs
    def get_object(self, request, *args, **kwargs):
        self._model = map_coop_model(kwargs['model'])
        try:
            self._mType = ContentType.objects.get(model=self._model)
        except Exception:
            pass
            # self._model is an abstract class. Lets find its subclasses
            # self._mType = []
            # ll = models.get_models()
            # TODO how to retrieve abstract class?
            # if self._model == u'contact':
            #     for l in ll:
            #         if pes.org.models.Contact in l.__mro__:
            #             self._mType.append(l)
        words = ['Updates for', self._model, 'on', Site.objects.get_current().name]
        self.title = _(' '.join(words))
        self.link = "/feed/%s/" % self._model
        return None



class UpdateFeedObject(Feed):
    title = _(u"Updates for %s." % Site.objects.get_current().name)
    link = "/feed/" 
    description = _(u"All records updates listed on the %s website." % Site.objects.get_current().name)
    hub = "http://%s/hub/" % Site.objects.get_current()



    def items(self):
        # Use ContenType to find the models .... If possible
        # ping dans save de model uri
        # TODO suppress the modified field and use sparql query to build
        # the selected items
        return get_model(self._mType.app_label, self._model).objects.filter(uri__icontains=self._uuid)
        # if not isinstance(self._mType, list):
        #     return get_model(self._mType.app_label, self._model).objects.filter(uri__icontains=self._uuid)
        # else:
        #     # self._mType should contains class
        #     res = []
        #     for t in self._mType:
        #         res.extend(t.objects.filter(uri__icontains=self._uuid))
        #     return res


    # to deal with overwriting ...
    def item_title(self, item):
        try:
            return item.label()
        except:
            return item.label

    def item_guid(self, item):
        scheme, host, path, query, fragment = urlsplit(item.uri)
        # path has the follong pathern : '/id/<class_name>/<uuid>/', so sp[3] is the uuid
        sp = path.split('/')
        try:
            return "%s_%s" % (sp[3], item.modified)
        except:
            return "%s_%s" % (path, item.modified)


    def item_description(self, item):
        return item.uri

    def item_link(self, item):
        return item.uri

    # def item_extra_kwargs
    def get_object(self, request, *args, **kwargs):
        self._model = map_coop_model(kwargs['model'])
        self._uuid = kwargs['obj']
        try:
            self._mType = ContentType.objects.get(model=self._model)
        except Exception:
            pass
            # self._model is an abstract class. Lets find its subclasses
            # self._mType = []
            # ll = models.get_models()
            # # TODO how to retrieve abstract class?
            # if self._model == u'contact':
            #     for l in ll:
            #         if pes.org.models.Contact in l.__mro__:
            #             self._mType.append(l)

        words = ['Updates for', self._model, 'on', Site.objects.get_current().name]
        self.title = _(' '.join(words))
        self.link = "/feed/%s/%s" % (self._model, self._uuid)
        return None




