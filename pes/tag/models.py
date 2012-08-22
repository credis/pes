# -*- coding:utf-8 -*-
# Create your models here.
from django.db import models
from django.db.models import IntegerField
from django.utils.translation import ugettext_lazy as _
from rdfalchemy import rdfSingle
from django.conf import settings
from djrdf.models import myRdfSubject, djRdf
from rdfalchemy.orm import mapper


class Tag(djRdf, myRdfSubject):
    # rdf attributes
    # rdf_type = settings.NS.skosxl.Label   #  move to the pes_local class
    label = rdfSingle(settings.NS.skosxl.literalForm)

    class Meta:

        abstract = True
        verbose_name = _(u'Tag')
        verbose_name_plural = _(u'Tags')


    def tagged(self, rdfType):
        """ returns the URI list from RDF resources using this tag
        filtered by rdfType
        """
        tagged = list(self.db.subjects(settings.NS.ess.tagged, self))
        model = mapper()[str(rdfType)]
        if tagged == []:
            return []
        else:
            res = []
            for e in tagged:
                one = list(self.db.triples((e, settings.NS.rdf.type, rdfType)))
                if one != []:
                    res.append(model(e))
            return res

    def org_tagged(self):
        return self.tagged(settings.NS.org.Organization)

   # django models attributes
    count = IntegerField(blank=True, null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('pes.tag.views.detailTag', [str(self.id)])

    # A special method to build a suggestion list from tag key words
    def addInWord(self):
        import pes
        words = set([])
        ws = self.label.split(' ')
        for w in ws:
            if len(w) >= 2:
                words.add(w.lower())
        for w in words:
            pes.models.Word.objects.get_or_create(name=w)

    # Idem save is overload to upgrade Word model in the same time.
    # The call to addInWord could also go in the post save signal.
    def save(self, *args, **kwargs):
        super(Tag, self).save(*args, **kwargs)
        if self.label:
            self.addInWord()
