#!/usr/bin/env python
import os.path
from os.path import join
from traceback import print_exc

from django import setup
from django.conf import settings
from django.test import TestCase
from django.test import Client
from importlib import resources
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from lxml.etree import DocumentInvalid
from lxml.etree import fromstring
from lxml.etree import parse
from lxml.etree import XMLSchema
from lxml.etree import XMLSyntaxError
from lxml.etree import XPath
from urllib.request import urlopen
import xmlschema

class APITestCase(TestCase):
    fixtures = ['test_data']

    @classmethod
    def setUpClass(cls):
        setup()
        super(APITestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(APITestCase, cls).tearDownClass()

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

        schema_root = parse(urlopen(settings.CENTRE_REGISTRY_XSD_URL))
        schema = xmlschema.XMLSchema(schema_root)

        for centre_info_url in centre_info_urls:
            response = client.get(centre_info_url, secure=True)
            self.assertEqual(response.status_code, 200)

            try:
                response.content.decode('utf-8')
                xml_doc = fromstring(response.content)
                schema.is_valid(xml_doc)

            except (XMLSyntaxError, DocumentInvalid):
                print_exc()
                self.fail()

    def test_centre(self):
        client = Client()
        response = client.get('/restxml/1/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

        schema_root = parse(urlopen(settings.CENTRE_REGISTRY_XSD_URL))
        schema = xmlschema.XMLSchema(schema_root)

        try:
            xml_doc = fromstring(response.content)
            schema.is_valid(xml_doc)
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
        schema = xmlschema.XMLSchema("https://schemas.opengis.net/kml/2.2.0/ogckml22.xsd")

        try:
            xml_doc = fromstring(response.content)
            schema.is_valid(xml_doc)
        except (XMLSyntaxError, DocumentInvalid):
            print_exc()
            self.fail()

    def test_get_model_centre(self):
        client = Client()
        response = client.get('/api/model/Centre', secure=True)
        self.assertEqual(response.status_code, 200)

        schema = json.loads(resources.files(__name__).joinpath('data', 'centres.json').read_bytes())

        centres_in_response = json.loads(response.content)
        try:
            validate(centres_in_response, schema)
        except ValidationError:
            print_exc()
            self.fail()

    def test_get_model_centretype(self):
        client = Client()
        response = client.get('/api/model/CentreType', secure=True)
        self.assertEqual(response.status_code, 200)

        schema = json.loads(resources.files(__name__).joinpath('data', 'centre_type.json').read_bytes())

        centre_types_in_response = json.loads(response.content)
        try:
            validate(centre_types_in_response, schema)
        except ValidationError:
            print_exc()
            self.fail()

    def test_get_model_contact(self):
        client = Client()
        response = client.get('/api/model/Contact', secure=True)
        self.assertEqual(response.status_code, 200)

        schema = json.loads(resources.files(__name__).joinpath('data', 'contact.json').read_bytes())

        contacts_in_response = json.loads(response.content)
        try:
            validate(contacts_in_response, schema)
        except ValidationError:
            print_exc()
            self.fail()

    def test_get_model_consortium(self):
        client = Client()
        response = client.get('/api/model/Consortium', secure=True)
        self.assertEqual(response.status_code, 200)

        schema = json.loads(resources.files(__name__).joinpath('data', 'consortium.json').read_bytes())

        consortiums_in_response = json.loads(response.content)
        try:
            validate(consortiums_in_response, schema)
        except ValidationError:
            print_exc()
            self.fail()

    def test_get_model_fcsendpoint(self):
        client = Client()
        response = client.get('/api/model/FCSEndpoint', secure=True)
        self.assertEqual(response.status_code, 200)

        schema = json.loads(resources.files(__name__).joinpath('data', 'fcsendpoint.json').read_bytes())

        fcsendpoints_in_response = json.loads(response.content)
        try:
            validate(fcsendpoints_in_response, schema)
        except ValidationError:
            print_exc()
            self.fail()

    def test_get_model_urlreference(self):
        client = Client()
        response = client.get('/api/model/URLReference', secure=True)
        self.assertEqual(response.status_code, 200)

        urlreferences_in_response = json.loads(response.content)

        schema = json.loads(resources.files(__name__).joinpath('data', 'urlreference.json').read_bytes())
        try:
            validate(urlreferences_in_response, schema)
        except ValidationError:
            print_exc()
            self.fail()

    def test_get_model_oaipmhendpoint(self):
        client = Client()
        response = client.get('/api/model/OAIPMHEndpoint', secure=True)
        self.assertEqual(response.status_code, 200)

        oaipmhendpoints_in_response = json.loads(response.content)
        schema = json.loads(resources.files(__name__).joinpath('data', 'oaipmhendpoint.json').read_bytes())
        try:
            validate(oaipmhendpoints_in_response, schema)
        except ValidationError:
            print_exc()
            self.fail()

    def test_get_model_samlidentityfederation(self):
        client = Client()
        response = client.get('/api/model/SAMLIdentityFederation', secure=True)
        self.assertEqual(response.status_code, 200)

        samlidentityfederations_in_response = json.loads(response.content)
        schema = json.loads(resources.files(__name__).joinpath('data', 'samlidentityfederation.json').read_bytes())
        try:
            validate(samlidentityfederations_in_response, schema)
        except ValidationError:
            print_exc()
            self.fail()

    def test_get_model_samlserviceprovider(self):
        client = Client()
        response = client.get('/api/model/SAMLServiceProvider', secure=True)
        self.assertEqual(response.status_code, 200)

        samlserviceproviders_in_response = json.loads(response.content)
        schema = json.loads(resources.files(__name__).joinpath('data', 'samlserviceprovider.json').read_bytes())
        try:
            validate(samlserviceproviders_in_response, schema)
        except ValidationError:
            print_exc()
            self.fail()
