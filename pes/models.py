# -*- coding:utf-8 -*-
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.db import models


# For suggestion purpose
class Word(models.Model):
    name = models.CharField(_(u'name'), blank=True, null=True, max_length=255, editable=False)

    def __unicode__(self):
        return unicode(self.name)

