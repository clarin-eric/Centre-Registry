#!/usr/bin/env python
from os.path import join
from traceback import print_exc

from django import setup
from django.core import serializers
from django.test import TestCase
from django.test import Client
import json
from lxml.etree import DocumentInvalid
from lxml.etree import fromstring
from lxml.etree import parse
from lxml.etree import XMLSchema
from lxml.etree import XMLSyntaxError
from lxml.etree import XPath
from pkg_resources import resource_string

from centre_registry.models import Centre
from centre_registry.models import CentreType
from centre_registry.models import Consortium
from centre_registry.models import AssessmentDates
from centre_registry.models import Contact
from centre_registry.models import FCSEndpoint
from centre_registry.models import MetadataFormat
from centre_registry.models import OAIPMHEndpoint
from centre_registry.models import SAMLIdentityFederation
from centre_registry.models import SAMLServiceProvider
from centre_registry.models import URLReference


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

    def test_get_model_centre(self):
        client = Client()
        response = client.get('/api/model/Centre', secure=True)
        self.assertEqual(response.status_code, 200)

        centres_in_response = json.loads(response.content)
        self.assertEqual(centres_in_response, json.loads(serializers.serialize('json', Centre.objects.all())))

    def test_get_model_centretype(self):
        client = Client()
        response = client.get('/api/model/CentreType', secure=True)
        self.assertEqual(response.status_code, 200)

        centre_types_in_response = json.loads(response.content)
        self.assertEqual(centre_types_in_response, json.loads(serializers.serialize('json', CentreType.objects.all())))

    def test_get_model_contact(self):
        client = Client()
        response = client.get('/api/model/Contact', secure=True)
        self.assertEqual(response.status_code, 200)

        contacts_in_response = json.loads(response.content)
        self.assertEqual(contacts_in_response, json.loads(serializers.serialize('json', Contact.objects.all())))

    def test_get_model_consortium(self):
        client = Client()
        response = client.get('/api/model/Consortium', secure=True)
        self.assertEqual(response.status_code, 200)

        consortiums_in_response = json.loads(response.content)
        self.assertEqual(consortiums_in_response, json.loads(serializers.serialize('json', Consortium.objects.all())))

    def test_get_model_fcsendpoint(self):
        client = Client()
        response = client.get('/api/model/FCSEndpoint', secure=True)
        self.assertEqual(response.status_code, 200)

        fcsendpoints_in_response = json.loads(response.content)
        self.assertEqual(fcsendpoints_in_response, json.loads(serializers.serialize('json', FCSEndpoint.objects.all())))

    def test_get_model_urlreference(self):
        client = Client()
        response = client.get('/api/model/URLReference', secure=True)
        self.assertEqual(response.status_code, 200)

        urlreferences_in_response = json.loads(response.content)
        self.assertEqual(urlreferences_in_response, json.loads(serializers.serialize('json', URLReference.objects.all())))

    def test_get_model_metadataformat(self):
        client = Client()
        response = client.get('/api/model/MetadataFormat', secure=True)
        self.assertEqual(response.status_code, 200)

        metadataformat_in_response = json.loads(response.content)
        self.assertEqual(metadataformat_in_response, json.loads(serializers.serialize('json', MetadataFormat.objects.all())))

    def test_get_model_oaipmhendpoint(self):
        client = Client()
        response = client.get('/api/model/OAIPMHEndpoint', secure=True)
        self.assertEqual(response.status_code, 200)

        oaipmhendpoint_in_response = json.loads(response.content)
        self.assertEqual(oaipmhendpoint_in_response, json.loads(serializers.serialize('json', OAIPMHEndpoint.objects.all())))

    def test_get_model_samlidentityfederation(self):
        client = Client()
        response = client.get('/api/model/SAMLIdentityFederation', secure=True)
        self.assertEqual(response.status_code, 200)

        samlidentityfederation_in_response = json.loads(response.content)
        self.assertEqual(samlidentityfederation_in_response, json.loads(serializers.serialize('json', SAMLIdentityFederation.objects.all())))

    def test_get_model_samlserviceprovider(self):
        client = Client()
        response = client.get('/api/model/SAMLServiceProvider', secure=True)
        self.assertEqual(response.status_code, 200)

        samlserviceprovider_in_response = json.loads(response.content)
        self.assertEqual(samlserviceprovider_in_response, json.loads(serializers.serialize('json', SAMLServiceProvider.objects.all())))

