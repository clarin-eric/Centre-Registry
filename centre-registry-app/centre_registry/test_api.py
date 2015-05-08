#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest


class APITestCase(unittest.TestCase):
    # fixtures = ['test_data']
    serialized_rollback = False
    # available_apps = ['centre_registry']

    @classmethod
    def setUpClass(cls):
        from django import setup
        from django.core import management

        setup()
        management.call_command('loaddata', 'test_data.json', verbosity=1, noinput=True)
        super(APITestCase, cls).setUpClass()

    # Tests for API v1
    def test_all_centres(self):
        from django.test import Client
        from lxml.etree import fromstring, XPath

        client = Client()
        response = client.get('/restxml/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

        xml_tree = fromstring(response.content)
        centre_info_url_xpath = XPath('/Centers/CenterProfile/Center_id_link/text()')
        centre_info_urls = centre_info_url_xpath(xml_tree)
        response = client.get(centre_info_urls[0], secure=True)
        self.assertEqual(response.status_code, 200)


    def test_centre(self):
        from django.test import Client
        from lxml.etree import fromstring, XMLParser, XMLSchema, XMLSyntaxError
        from os.path import join
        from pkg_resources import resource_string
        from traceback import print_exc

        client = Client()
        response = client.get('/restxml/1/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

        schema_root = fromstring(resource_string(__name__, join('data', 'CenterProfile.xsd')))
        schema = XMLSchema(schema_root)

        parser = XMLParser(schema=schema)
        try:
            fromstring(response.content, parser)
        except XMLSyntaxError:
            print_exc()
            self.fail()

    # Tests for API v2
    def test_centres_kml(self):
        from django.test import Client
        from lxml.etree import fromstring, parse, XMLParser, XMLSchema, XMLSyntaxError
        from traceback import print_exc

        client = Client()
        response = client.get('/api/KML/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.google-earth.kml+xml')

        # It is necessary to load this KML XSD over HTTP as it imports two other XSDs using relative names, which
        # does not work well with Python package resources, that should not be located to an absolute location.
        schema_doc = parse("http://www.opengis.net/kml/2.2")
        schema = XMLSchema(schema_doc)

        parser = XMLParser(schema=schema)
        try:
            fromstring(response.content, parser)
        except XMLSyntaxError:
            print_exc()
            self.fail()

    def test_model(self):
        from django.test import Client

        client = Client()
        response = client.get('/api/model/Centre', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')