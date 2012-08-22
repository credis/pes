# -*- coding:utf-8 -*-
# Create your models here.
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rdfalchemy import rdfMultiple
from django.conf import settings
from djrdf.models import myRdfSubject, djRdf
import rdflib


if not hasattr(settings, 'RDF_DEFAULT_LANG'):
    setattr(settings, 'RDF_DEFAULT_LANG', settings.LANGUAGE_CODE.split('-')[0])



class Concept(djRdf, myRdfSubject):
    # rdf_type = settings.NS.skos.Concept
    inScheme = rdfMultiple(settings.NS.skos.inScheme, range_type=settings.NS.skos.ConceptScheme)
    topConceptOf = rdfMultiple(settings.NS.skos.topConceptOf, range_type=settings.NS.skos.ConceptScheme)
    prefLabels = rdfMultiple(settings.NS.skosxl.prefLabel, range_type=settings.NS.skosxl.Label)
    altLabels = rdfMultiple(settings.NS.skosxl.altLabel, range_type=settings.NS.skosxl.Label)
    hiddenLabels = rdfMultiple(settings.NS.skosxl.hiddenLabel, range_type=settings.NS.skosxl.Label)

    broader = rdfMultiple(settings.NS.skos.broader, range_type=settings.NS.skos.Concept)
    narrower = rdfMultiple(settings.NS.skos.narrower, range_type=settings.NS.skos.Concept)
    related = rdfMultiple(settings.NS.skos.related, range_type=settings.NS.skos.Concept)
    # TODO do we need this attributes?
    # broaderTrans = rdfMultiple(skos.broaderTransitive, range_type= skos.Concept)
    # narrowerTrans = rdfMultiple(skos.narrowerTransitive, range_type= skos.Concept)
    # semanticRel = rdfMultiple(skos.semanticRelation, range_type= skos.Concept)

    notation = rdfMultiple(settings.NS.skos.notation)
    note = rdfMultiple(settings.NS.skos.note)
    definition = rdfMultiple(settings.NS.skos.definition)
    example = rdfMultiple(settings.NS.skos.example)

    def _get_prefLabel(self):
        pref = self.prefLabels
        if len(pref) == 0:
            return None
        elif len(pref) == 1:
            return pref[0]
        else:
            for label in pref:
                literal = self.bd.objects(label, settings.NS.skosxl.literalForm)[0]
                assert(isinstance(literal, rdflib.term.Literal))
                if literal.language == settings.RDF_DEFAULT_LANG:
                    return label

    prefLabel = property(_get_prefLabel)

    @models.permalink
    def get_absolute_url(self):
        return ('pes.thess.views.detailConcept', [str(self.id)])

    class Meta:
        verbose_name = _(u'concept')
        verbose_name_plural = _(u'concepts')




class Scheme(myRdfSubject):
    # rdf_type = settings.NS.skos.ConceptScheme

    # An attribute label is already added with the help of myRdfSubject class
    hasTopConcept = rdfMultiple(settings.NS.skos.hasTopConcept, range_type=settings.NS.skos.Concept)

    # I guess, we have no information about the context of the scheme subject....
    # From the db, we can try to find it....
    # The normal case is when the scheme is defined in a context, so we should find
    # this context
    def _get_context(self):
        tr = list(self.db.triples((self, settings.NS.rdf.type, settings.NS.skos.ConceptScheme)))
        ctx = self.db.contexts
        if len(tr) == 0:
            raise Exception(_(u'get_context for scheme, no triples, invalid case'))
        elif len(tr) == 1:
            if len(ctx) == 0:
                # No context has been set.... why not?
                return None
            elif len(ctx) == 1:
                verif = list(self.db.triples((self, settings.NS.rdf.type, settings.NS.skos.ConceptScheme), ctx[0]))
                if len(verif) == 1:
                    return ctx[0]
                else:
                    raise Exception(_(u'context not found for scheme %s and contexts' % (repr(self), ctx)))
            else:
                # Find the concept associate with the triple
                for c in ctx:
                    verif = list(self.db.triples((self, settings.NS.rdf.type, settings.NS.skos.ConceptScheme), c))
                    if len(verif) == 1:
                        return c
                raise Exception(_(u'context not found for scheme %s' % repr(self)))
        else:
            # The scheme is defined in many context....
            # This configuration is not handled yet....
            raise Exception(_(u'Scheme %s defined in many conctexts, not handled yes' % self))

    context = property(_get_context)

    def _get_concepts(self):
        return list(self.db.subjects(settings.NS.skos.inScheme, self))

    concepts = property(_get_concepts)


