# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from djrdf.forms import djRdfForm, posint
from pes_local.models import  Tag
from formalchemy import types
from formalchemy.ext.rdf import  Field, RdfFieldRenderer, RdfSelectFieldRenderer



class OrgForm(djRdfForm):
    # model = Organization

    def _configure(self, fs):
        if fs.model.description != None:
            desc_size = "100x%s" % (len(fs.model.description) / 50)
        else:
            desc_size = "100x10"

        fs.append(Field('marks', type=types.Integer).validate(posint))
        fs.append(Field('description'))
        fs.append(Field('tags'))
        fs.append(Field('seeks'))
        fs.append(Field('offers'))
        fs.append(Field('members'))
 
        # TODO add fs.contacts... still waiting for d2r condition bugs
        fs.configure(include=[fs.description, fs.tags, fs.seeks, fs.offers,  fs.marks, fs.members],
            options=[
                fs.description.textarea(size=desc_size).readonly(value=False),
                fs.tags.set(multiple=True, options=map(lambda x: (x.label, x), Tag.objects.all())),
                fs.members.set(multiple=True, options=map(lambda x: (x.name, x), fs.model.members)),
                # fs.contacts.set(multiple=True, options=map(lambda x: (x.content, x), fs.model.contacts)),
                fs.seeks.set(multiple=True, options=map(lambda x: (x.title, x), fs.model.seeks)),
                fs.offers.set(multiple=True, options=map(lambda x: (x.title, x), fs.model.offers)),
                ])
        fs.tags._renderer = RdfSelectFieldRenderer
        fs.members._renderer = RdfSelectFieldRenderer
        # fs.contacts._renderer = RdfSelectFieldRenderer
        fs.seeks._renderer = RdfSelectFieldRenderer
        fs.offers._renderer = RdfSelectFieldRenderer
 
        return fs


