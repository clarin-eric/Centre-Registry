from collections import OrderedDict
from json import loads
from urllib.request import urlopen

from centre_registry.models import Centre
from centre_registry.models import Consortium
from centre_registry.models import Contact
from centre_registry.models import FCSEndpoint
from centre_registry.models import OAIPMHEndpointSet
from centre_registry.models import SAMLIdentityFederation
from centre_registry.models import SAMLServiceProvider
from centre_registry.models import URLReference
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import RequestContext


def get_about(request):
    request_context = RequestContext(request, {'view': 'about'})
    return render(
        request, template_name='UI/_about.html', context=request_context.flatten())


def get_all_centres(request):
    request_context = RequestContext(request, {'view': 'all_centres',
                                               'all_centres':
                                               Centre.objects.all()})
    return render(
        request, template_name='UI/_all_centres.html', context=request_context.flatten())


def get_centre(request, centre_id):
    centre = get_object_or_404(Centre, pk=centre_id)
    request_context = RequestContext(
        request, {'view': 'centre',
                  'centre': centre,
                  'url_references':
                  URLReference.objects.filter(centre__pk=centre.pk)})
    return render(
        request, template_name='UI/_centre.html', context=request_context.flatten())


def get_centres_contacts(request):
    request_context = RequestContext(request, {'view': 'centres_contacts',
                                               'all_centres':
                                               Centre.objects.all()})
    return render(
        request,
        template_name='UI/_centres_contacts.html',
        context=request_context.flatten())


def get_consortia(request):
    request_context = RequestContext(request, {'view': 'consortia',
                                               'consortia':
                                               Consortium.objects.all()})
    return render(
        request, template_name='UI/_consortia.html', context=request_context.flatten())


def get_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    request_context = RequestContext(request, {'view': 'contact',
                                               'contact': contact})
    return render(
        request, template_name='UI/_contact.html', context=request_context.flatten())


def get_contacting(request):
    request_context = RequestContext(request, {'view': 'contacting'})
    return render(
        request, template_name='UI/_contacting.html', context=request_context.flatten())


def get_fcs(request):
    request_context = RequestContext(request, {'view': 'fcs',
                                               'fcs_endpoints':
                                               FCSEndpoint.objects.all()})
    return render(
        request, template_name='UI/_fcs.html', context=request_context.flatten())


def get_oai_pmh(request):
    request_context = RequestContext(request, {'view': 'oai_pmh',
                                               'oai_pmh_endpoints_sets':
                                               OAIPMHEndpointSet.objects.all()})
    return render(
        request, template_name='UI/_oai_pmh.html', context=request_context.flatten())


def get_map(request):
    request_context = RequestContext(
        request, {'view': 'map',
                  'url_prefix': request.build_absolute_uri('/').replace('http://', 'https://')})
    return render(
        request, template_name='UI/_map.html', context=request_context.flatten())


def get_spf(request):
    processed_sps_across_id_feds = loads(
        urlopen('https://infra.clarin.eu/aai/sps_at_identity_federations/'
                'summary.json').read().decode('utf-8'))

    saml_id_feds = SAMLIdentityFederation.objects \
        .filter(shorthand__in=processed_sps_across_id_feds) \
        .extra(select={'shorthand_lower': 'lower(shorthand)'}) \
        .order_by('shorthand_lower') \
        .all()

    # TODO: handle exceptions
    id_feds_also_in_summary = \
        {saml_id_fed.shorthand: processed_sps_across_id_feds[
            saml_id_fed.shorthand] for saml_id_fed in saml_id_feds}

    processed_sps_across_id_feds2 = \
        OrderedDict(sorted(
            id_feds_also_in_summary.items(),
            key=lambda id_fed_shorthand:
            id_fed_shorthand[0].lower()))

    request_dict = {'view': 'spf',
                    'saml_service_providers':
                    SAMLServiceProvider.objects.all(),
                    'saml_id_feds':
                    saml_id_feds,
                    'processed_sps_across_id_feds':
                    processed_sps_across_id_feds2}
    request_context = RequestContext(request, request_dict)
    return render(
        request, template_name='UI/_spf.html', context=request_context.flatten())
