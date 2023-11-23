import logging
from collections import OrderedDict
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import RequestContext
from json import loads
from urllib.request import urlopen
import requests
from typing import Union

from centre_registry.forms import KCentreForm
from centre_registry.models import Centre
from centre_registry.models import Consortium
from centre_registry.models import Contact
from centre_registry.models import FCSEndpoint
from centre_registry.models import KCentre
from centre_registry.models import OAIPMHEndpoint
from centre_registry.models import SAMLIdentityFederation
from centre_registry.models import SAMLServiceProvider
from centre_registry.models import ShadowKCentre
from centre_registry.models import URLReference
from centre_registry.utils import get_object_or_None
from centre_registry.views_api import post_kcentre_form


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


def get_all_kcentres(request):
    request_context: RequestContext = RequestContext(request,
                                                     {'view': 'all_kcentres',
                                                      'all_kcentres':
                                                          KCentre.objects.all()})

    return render(
        request, template_name='UI/_all_kcentres.html', context=request_context.flatten())


def get_centre(request, centre_id):
    centre = get_object_or_404(Centre, pk=centre_id)
    request_context = RequestContext(
        request, {'view': 'centre',
                  'centre': centre,
                  'url_references':
                      URLReference.objects.filter(centre__pk=centre.pk)})
    return render(
        request,
        template_name='UI/_centre.html',
        context=request_context.flatten())


def get_kcentre(request, kcentre_id):
    kcentre = get_object_or_404(KCentre, pk=kcentre_id)
    centre = kcentre.centre_fk
    request_context = RequestContext(
        request, {'view': 'kcentre',
                  'centre': centre,
                  'kcentre': kcentre}
    )
    return render(
        request,
        template_name='UI/_kcentre.html',
        context=request_context.flatten())


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
        request,
        template_name='UI/_consortia.html',
        context=request_context.flatten())


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
    fcs_endpoints = FCSEndpoint.objects.all()
    centre_fcs_endpoints_dict = {}

    for endpoint in fcs_endpoints:
        centre = endpoint.centre
        if not centre:
            centre = "NoCentre"
        if centre in centre_fcs_endpoints_dict.keys():
            centre_fcs_endpoints_dict[centre].append(endpoint)
        else:
            centre_fcs_endpoints_dict[centre] = [endpoint]

    request_context = RequestContext(request, {'view': 'fcs',
                                               'fcs_endpoints':
                                                   FCSEndpoint.objects.all(),
                                               'centre_fcs_endpoints_dict':
                                                   centre_fcs_endpoints_dict})
    return render(
        request, template_name='UI/_fcs.html', context=request_context.flatten())


def get_oai_pmh(request):
    oai_pmh_endpoints = OAIPMHEndpoint.objects.all()
    centre_endpoints_dict = {}
    endpoint_sets_dict = {}

    for endpoint in oai_pmh_endpoints:
        centre = endpoint.centre
        if not centre:
            centre = "NoCentre"
        if centre in centre_endpoints_dict.keys():
            centre_endpoints_dict[centre].append(endpoint)
        else:
            centre_endpoints_dict[centre] = [endpoint]

    for endpoint in oai_pmh_endpoints:
        if endpoint in endpoint_sets_dict.keys():
            endpoint_sets_dict[endpoint].append(endpoint.oai_pmh_sets.all())
        else:
            endpoint_sets_dict[endpoint] = list(endpoint.oai_pmh_sets.all())

    request_context = RequestContext(request, {'view': 'oai_pmh',
                                               'centre_endpoints_dict':
                                                   centre_endpoints_dict,
                                               'endpoint_sets_dict':
                                                   endpoint_sets_dict,
                                               'oai_pmh_endpoints':
                                                   oai_pmh_endpoints})
    return render(
        request, template_name='UI/_oai_pmh.html', context=request_context.flatten())


def get_map(request):
    request_context = RequestContext(
        request, {'view': 'map',
                  'url_prefix': request.build_absolute_uri('/').replace('http://', 'https://')})
    return render(
        request, template_name='UI/_map.html', context=request_context.flatten())


def get_spf(request):
    saml_service_providers = SAMLServiceProvider.objects.all()
    centre_saml_providers_dict = {}

    for endpoint in saml_service_providers:
        centre = endpoint.centre
        if not centre:
            centre = "NoCentre"
        if centre in centre_saml_providers_dict.keys():
            centre_saml_providers_dict[centre].append(endpoint)
        else:
            centre_saml_providers_dict[centre] = [endpoint]

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
                        saml_service_providers,
                    'centre_saml_providers_dict':
                        centre_saml_providers_dict,
                    'saml_id_feds':
                        saml_id_feds,
                    'processed_sps_across_id_feds':
                        processed_sps_across_id_feds2}
    request_context = RequestContext(request, request_dict)
    return render(
        request, template_name='UI/_spf.html', context=request_context.flatten())


def get_kcentre_edit_form(request: HttpRequest, kcentre_id=None) -> HttpResponse:
    kcentre = None
    if kcentre_id is not None:
        kcentre = get_object_or_None(KCentre, pk=kcentre_id)
    kcentre_form: KCentreForm = KCentreForm(request.GET)
    request_context: RequestContext = RequestContext(request, {"kcentre": kcentre})
    if kcentre_form.is_valid():
        kcentre_form_data = kcentre_form.cleaned_data
        kcentre_form_data['kcentre_fk'] = kcentre
        request_context.push({"kcentre_form_data": kcentre_form_data})

        # create and save KCentre's shadow instance, creation of related handled by exposing
        # admin widget to ShadowModels in the form
        return post_kcentre_form(request, request_context.flatten())

    else:
        if kcentre is not None:
            kcentre_form = KCentreForm(instance=kcentre)
        request_context.push({"kcentre_form": kcentre_form})

    return render(request, template_name='UI/_kcentre_edit_form.html', context=request_context.flatten())
