#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join
from pkg_resources import resource_string
from traceback import print_exc
import unittest

from django.core import management
from django.test import Client
from django import setup
from lxml.etree import DocumentInvalid
from lxml.etree import fromstring
from lxml.etree import parse
from lxml.etree import XMLSchema
from lxml.etree import XMLSyntaxError
from lxml.etree import XPath


class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup()
        management.call_command('loaddata', 'test_data.json', verbosity=1,
                                noinput=True)
        super(APITestCase, cls).setUpClass()

    # Tests for API v1
    def test_all_centres(self):
        client = Client()
        response = client.get('/restxml/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

        xml_tree = fromstring(response.content)
        centre_info_url_xpath = XPath(
            '/Centers/CenterProfile/Center_id_link/text()')
        centre_info_urls = centre_info_url_xpath(xml_tree)
        response = client.get(centre_info_urls[0], secure=True)
        self.assertEqual(response.status_code, 200)

    def test_centre(self):
        client = Client()
        response = client.get('/restxml/1/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

        schema_root = fromstring(
            resource_string(__name__, join('data', 'CenterProfile.xsd')))
        schema = XMLSchema(schema_root)

        try:
            xml_doc = fromstring(response.content)
            schema.assertValid(xml_doc)
        except (XMLSyntaxError, DocumentInvalid):
            print_exc()
            self.fail()

    # Tests for API v2
    def test_centres_kml(self):
        client = Client()
        response = client.get('/api/KML/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'],
                         'application/vnd.google-earth.kml+xml')

        # It is necessary to load this KML XSD over HTTP as it imports two
        # other XSDs using relative names, which
        # does not work well with Python package resources, that should not
        # be located to an absolute location.
        schema_doc = parse("http://www.opengis.net/kml/2.2")
        schema = XMLSchema(schema_doc)

        try:
            xml_doc = fromstring(response.content)
            schema.assertValid(xml_doc)
        except (XMLSyntaxError, DocumentInvalid):
            print_exc()
            self.fail()

    def test_model(self):
        client = Client()
        response = client.get('/api/model/Centre', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
