# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from djrdf.forms import djRdfForm
from pes_local.models import  Tag
from formalchemy.ext.rdf import  Field, RdfFieldRenderer, RdfSelectFieldRenderer



class TitleRdfFieldRenderer(RdfFieldRenderer):
    """render a rdf field  as a text field"""

    # publisher is an Organization, so it has a title field which gives its name
    def stringify_value(self, v):
        return v.title


class ExchangeForm(djRdfForm):
    # model = Exchange

    def _configure(self, fs):
        if fs.model.description != None:
            desc_size = "100x%s" % (len(fs.model.description) / 50)
        else:
            desc_size = "100x10"

        fs.append(Field('description'))
        fs.append(Field('tags'))
        fs.append(Field('title'))
        fs.append(Field('area'))
        fs.append(Field('publisher'))

        # TODO add fs.contacts... still waiting for d2r condition bugs
        fs.configure(include=[fs.description, fs.tags, fs.title, fs.area, fs.publisher],
            options=[
                fs.description.textarea(size=desc_size).readonly(value=False),
                fs.tags.set(multiple=True, options=map(lambda x: (x.label, x), Tag.objects.all())),
                ])
        fs.tags._renderer = RdfSelectFieldRenderer
        fs.publisher._renderer = TitleRdfFieldRenderer
        return fs
