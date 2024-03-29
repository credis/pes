# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from djrdf.forms import djRdfForm, posint
from pes_local.models import Tag
from formalchemy import types
from formalchemy.ext.rdf import  Field


class TagForm(djRdfForm):
    model = Tag

    def _configure(self, fs):
       # None rdfSubject fields have to be added
        fs.append(Field('count', type=types.Integer))
        # Same thing for field inheriting from a mother class
        fs.append(Field('name').label(u'nom'))  # _() ne marche pas???
        # fs.configure(include=[fs.name, fs.count.validate(posint)])
        fs.configure(include=[fs.name])
        return fs
