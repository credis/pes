# -*- coding:utf-8 -*-
# from djrdf.models import FlyAttr
import rdfalchemy
from   djrdf.repository import Repository
from django.conf import settings


rdfalchemy.rdfSubject.db = Repository(settings.SESAME_REPOSITORY_NAME)
