# -*- coding:utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from pes.org.models import *
from sesame import *



def init():
    oo = Organization.ClassInstances()
    for o in oo:
        print o.title
        o.save()
    tt = Tag.ClassInstances()
    for t in tt:
        print t.label
        t.save()


class OrganizationTest(TestCase):
    # We suppose that the repository is not empty
    # Manual or by set_up load the famous dump-sav.nt file
    def setUp(self):
        pass
        # print "SET UP DONE"
        # pesSesame.load(source='dump-sav.nt', format="n3", publicID='file:///context')
        # pesSesame.load(source='dump-sav.nt', format="n3")

    # Check read feature
    def test_read(self):
        oo = Organization.ClassInstances()
        o1 = oo.next()
        title = o1.title

        o2 = oo.next()
        title2 = o2.title
        self.assertNotEqual(title, title2, "check that o1 and o2 are differents uri ")
        self.assertNotEqual(o1.label, o2.label)

        # check that o1 and o2 are in django bd
        o1.save()
        o2.save()
        o3 = Organization.objects.get(uri=o1.uri)
        print o3.resUri
        print o1.resUri
        self.assertEqual(o3.title, o1.title)
        self.assertEqual(o3.resUri, o1.resUri)

        o4 = Organization.objects.get(uri=o2.uri)
        self.assertEqual(o4.label, o2.label)
        self.assertEqual(o4.logo, o2.logo)

        # Search by attributes
        for o in oo:
            print o.title
            o.save()
        o = Organization.get_by(label="Études et Chantiers")
        self.assertEqual(o.tags.__len__(), 2)
        self.assertEqual(o.homepage, "http://www.unarec.org/espace_centre/index.php")

        ms = Membership.ClassInstances()
        m1 = ms.next()
        m1 = ms.next()
        m1 = ms.next()
        m1 = ms.next()
        m1 = ms.next()
        o1 = Organization.get_by(label=m1.organization.label)
        self.assertEqual(m1.organization.title, o1.title)
        self.assertEqual(m1.organization.description, o1.description)
        o1.save()
        # Now o1 is store in django database

        # tt = Tag.ClassInstances()
        # for t in tt:
        #         print t.label

