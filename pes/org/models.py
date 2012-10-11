# -*- coding:utf-8 -*-
# Create your models here.
from django.db import models
from django.db.models import IntegerField
from django.utils.translation import ugettext_lazy as _
from rdfalchemy import rdfSingle, rdfMultiple
from django.conf import settings
from djrdf.models import myRdfSubject, djRdf


# Warning the order of the classes is MANDATORY
class Organization(djRdf, myRdfSubject):
    # rdf attributes
    # rdf_type = settings.NS.org.Organization

    label = rdfSingle(settings.NS.rdfs.label)
    description = rdfSingle(settings.NS.dct.description)
    tags = rdfMultiple(settings.NS.dct.subject, range_type=settings.NS.skosxl.Label)
    # abstract = rdfSingle(DCT.abstract)  # wait for issue #208 of rdflib
    web = rdfSingle(settings.NS.foaf.homepage)
    logo = rdfSingle(settings.NS.foaf.logo)
    title = rdfSingle(settings.NS.legal.legalName)
    acronym = rdfSingle(settings.NS.ov.prefAcronym)
    pref_address = rdfSingle(settings.NS.legal.registeredAddress, range_type=settings.NS.locn.Address)
    location = rdfMultiple(settings.NS.locn.location, range_type=settings.NS.dct.Location)
    seeks = rdfMultiple(settings.NS.gr.seeks, range_type=settings.NS.ess.Exchange)
    offers = rdfMultiple(settings.NS.gr.offers, range_type=settings.NS.ess.Exchange)
    members = rdfMultiple(settings.NS.org.hasMember, range_type=settings.NS.person.Person)
    comment = rdfMultiple(settings.NS.rdfs.comment)
    # contacts = rdfMultiple(settings.NS.ess.hasContactMedium, range_type=settings.NS.ess.ContactMedium)

    # django models attributes
    marks = IntegerField(blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = _(u'Organization')
        verbose_name_plural = _(u'Organizations')

    @property
    def roles(self):
        return map(Membership, list(self.db.subjects(settings.NS.org.organization, self)))

    @property
    def contacts(self):
        return list(self.db.objects(self, NS.ess.hasContactMedium))

    @models.permalink
    def get_absolute_url(self):
        return ('pes.org.views.detailOrg', [str(self.id)])



class Contact(djRdf, myRdfSubject):
    rdf_type = settings.NS.ess.ContactMedium
    details = rdfMultiple(settings.NS.rdfs.comment)
    content = rdfSingle(settings.NS.rdf.value)

    class Meta:
        abstract = True




class Membership(myRdfSubject):
    rdf_type = settings.NS.org.Membership
    member = rdfSingle(settings.NS.org.member, range_type=settings.NS.person.Person)
    role = rdfSingle(settings.NS.org.role, range_type=settings.NS.org.Role)
    organization = rdfSingle(settings.NS.org.organization, range_type=settings.NS.org.Organization)
    description = rdfSingle(settings.NS.dct.description)


class Role(myRdfSubject):
    rdf_type = settings.NS.org.Role
    label = rdfSingle(settings.NS.rdfs.label)


class Person(djRdf, myRdfSubject):
    # rdf_type = settings.NS.person.Person  # on peut aussi bien ecrire rdf_type = FOAF.Person
    name = rdfSingle(settings.NS.foaf.familyName)

    class Meta:
        abstract = True




from django_push.subscriber.signals import updated
from pes.signals import listener
updated.connect(listener)


