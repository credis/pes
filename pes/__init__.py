# -*- coding:utf-8 -*-
import rdfalchemy
from   djrdf.repository import Repository
from django.conf import settings


rdfalchemy.rdfSubject.db = Repository(settings.SESAME_REPOSITORY_NAME)
