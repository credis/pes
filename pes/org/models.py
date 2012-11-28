# -*- coding:utf-8 -*-
# Create your models here.
from django.db import models
from django.db.models import IntegerField
from django.utils.translation import ugettext_lazy as _
from rdfalchemy import rdfSingle, rdfMultiple
from django.conf import settings
from djrdf.models import myRdfSubject, djRdf
from pes.utils import addr_to_point, loc_to_point
from rdflib import URIRef
import logging

log = logging.getLogger('pes')


# Warning the order of the classes is MANDATORY
class Organization(djRdf, myRdfSubject):
    # rdf attributes
    # rdf_type = settings.NS.org.Organization

    label = rdfSingle(settings.NS.rdfs.label)
    description = rdfSingle(settings.NS.dct.description)
    tags = rdfMultiple(settings.NS.dct.subject, range_type=settings.NS.skosxl.Label)
    abstract = rdfSingle(URIRef(str(settings.NS['dct']) + 'abstract'))
    homepage = rdfSingle(settings.NS.foaf.homepage)
    logo = rdfSingle(settings.NS.foaf.logo)
    title = rdfSingle(settings.NS.legal.legalName)
    acronym = rdfSingle(settings.NS.ov.prefAcronym)
    pref_address = rdfSingle(settings.NS.legal.registeredAddress, range_type=settings.NS.locn.Address)
    location = rdfMultiple(settings.NS.locn.location, range_type=settings.NS.dct.Location)
    seeks = rdfMultiple(settings.NS.gr.seeks, range_type=settings.NS.ess.Exchange)
    offers = rdfMultiple(settings.NS.gr.offers, range_type=settings.NS.ess.Exchange)
    members = rdfMultiple(settings.NS.org.hasMember, range_type=settings.NS.person.Person)
    comment = rdfMultiple(settings.NS.rdfs.comment)
    identifiers = rdfMultiple(settings.NS.org.identifier)
    notes = rdfSingle(settings.NS.skos.note)
    contacts = rdfMultiple(settings.NS.ess.hasContactMedium, range_type=settings.NS.ess.ContactMedium)

    # django models attributes
    marks = IntegerField(blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = _(u'Organization')
        verbose_name_plural = _(u'Organizations')

    @property
    def web(self):
        try:
            if self.homepage:
                return unicode(self.homepage.resUri)
        except Exception, e:
            log.debug("Error accessing homepage field of %s : %s" % (self.uri, e))

    @property
    def roles(self):
        return map(Engagement, list(self.db.subjects(settings.NS.org.organization, self)))

    # @property
    # def contacts(self):
    #     return list(self.db.objects(self, settings.NS.ess.hasContactMedium))

    @models.permalink
    def get_absolute_url(self):
        return ('pes.org.views.detailOrg', [str(self.id)])

    @property
    def geo_point(self):
        if self.pref_address:
            return addr_to_point(self.pref_address)
        elif self.location and len(self.location) > 0:
            return loc_to_point(self.location[0])

    def to_geoJson(self):
        if self.geo_point:
            return {
               "type": "Feature",
                "properties": {
                        "name": self.title.encode('utf-8'),
                        "popupContent": "<h4>" + self.title.encode('utf-8') + "</h4><p><a href='" + self.get_absolute_url() + "'>" + self.title.encode('utf-8') + "</a></p>"
                        },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [self.geo_point.x, self.geo_point.y]
                        }
                    }







class Contact(djRdf, myRdfSubject):
    # rdf_type = settings.NS.ess.ContactMedium
    details = rdfMultiple(settings.NS.rdfs.comment)
    content = rdfSingle(settings.NS.rdf.value)

    contact_mapping = {
        settings.NS.vcard.Cell: _(u'cell'),
        settings.NS.vcard.Fax: _(u'fax'),
        settings.NS.ess.Skype: _(u'skype'),
        settings.NS.ov.MicroblogPost: _(u'twitter'),
        settings.NS.rss.Channel: _(u'rss'),
        settings.NS.vcal.Vcalendar: _(u'ics'),
        settings.NS.vcard.Email: _(u'email'),
        settings.NS.sioc.Site: _(u'web'),
        settings.NS.vcard.Tel: _(u'phone')
    }

    class Meta:
        abstract = True

    @property
    def label(self):
        return self.content

    def contact_type(self):
        types = list(self.db.triples((self, settings.NS.rdf.type, None)))
        types.remove((URIRef(self.uri), settings.NS.rdf.type, self.rdf_type))
        return self.contact_mapping[types[0][2]]




class Engagement(myRdfSubject):
    rdf_type = settings.NS.org.Membership
    member = rdfSingle(settings.NS.org.member, range_type=settings.NS.person.Person)
    role = rdfSingle(settings.NS.org.role, range_type=settings.NS.org.Role)
    organization = rdfSingle(settings.NS.org.organization, range_type=settings.NS.org.Organization)
    description = rdfSingle(settings.NS.dct.description)


class Role(myRdfSubject):
    rdf_type = settings.NS.org.Role
    label = rdfSingle(settings.NS.skos.prefLabel)


class Person(djRdf, myRdfSubject):
    # rdf_type = settings.NS.person.Person  # on peut aussi bien ecrire rdf_type = FOAF.Person
    name = rdfSingle(settings.NS.foaf.familyName)
    full_name = rdfSingle(settings.NS.foaf.name)
    tags = rdfMultiple(settings.NS.dct.subject, range_type=settings.NS.skosxl.Label)
    location = rdfMultiple(settings.NS.locn.location, range_type=settings.NS.dct.Location)
    notes = rdfSingle(settings.NS.skos.note)
    contacts = rdfMultiple(settings.NS.ess.hasContactMedium, range_type=settings.NS.ess.ContactMedium)

    class Meta:
        abstract = True

    @models.permalink
    def get_absolute_url(self):
        return ('pes.org.views.detailPerson', [str(self.id)])

    @property
    def label(self):
        return self.full_name

    @property
    def geo_point(self):
        if self.location and len(self.location) > 0:
            return loc_to_point(self.location[0])
        # on peut forcer et utiliser la localization de l'organization

    def to_geoJson(self):
        if self.geo_point:
            return {
               "type": "Feature",
                "properties": {
                        "name": self.full_name.encode('utf-8'),
                        "popupContent": "<h4>" + self.full_name.encode('utf-8') + "</h4><p><a href='" + self.get_absolute_url() + "'>" + self.full_name.encode('utf-8') + "</a></p>"
                        },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [self.geo_point.x, self.geo_point.y]
                        }
                    }




from django_push.subscriber.signals import updated
from pes.signals import listener
updated.connect(listener)


