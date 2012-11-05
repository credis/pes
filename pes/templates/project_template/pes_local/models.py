# -*- coding:utf-8 -*-
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from pes.exchange.models import Exchange as BaseExchange
from pes.org.models import Organization as BaseOrganization
from pes.org.models import Contact
from pes.org.models import Person as BasePerson
from pes.tag.models import Tag as BaseTag
from pes.thess.models import Concept as BaseConcept
from pes.article.models import Article as BaseArticle
from pes.article.models import Product as BaseProduct
from rdfalchemy.orm import mapper
import pes.geo.models    # Mandatory to build the RDFAlchemy mapper

# Becareful for rdfalchemy mapper, the rdf_type attribut HAS to be set here


class Product(BaseProduct):
    rdf_type = settings.NS.schema.Product


class Article(BaseArticle):
    rdf_type = settings.NS.dct.Text



class Exchange(BaseExchange):
    rdf_type = settings.NS.ess.Exchange
 

class Organization(BaseOrganization):
    rdf_type = settings.NS.org.Organization



class Tel(Contact):
    rdf_type = settings.NS.vcard.Tel


class Cell(Contact):
    rdf_type = settings.NS.vcard.Cell


class Fax(Contact):
    rdf_type = settings.NS.vcard.Fax


class Skype(Contact):
    rdf_type = settings.NS.ess.Skype


class Twitter(Contact):
    rdf_type = settings.NS.ov.MicroblogPost


class Rss(Contact):
    rdf_type = settings.NS.rss.Channel


class Cal(Contact):
    rdf_type = settings.NS.vcal.Calendar


class Email(Contact):
    rdf_type = settings.NS.vcard.Email


class Web(Contact):
    rdf_type = settings.NS.sioc.Site


class Person(BasePerson):
    rdf_type = settings.NS.person.Person  # on peut aussi bien ecrire rdf_type = FOAF.Person


class Tag(BaseTag):
    rdf_type = settings.NS.skosxl.Label


class Concept(BaseConcept):
    rdf_type = settings.NS.skos.Concept


# This MANDATORY to link attributes trought the rdfSubject instances
mapper()



