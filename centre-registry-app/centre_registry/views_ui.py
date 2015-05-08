# -*- coding: utf-8 -*-


def get_about(request):
    from django.shortcuts import render
    from django.template import RequestContext

    request_context = RequestContext(request, {'view': 'about'})

    return render(request,
                  template_name='UI/_about.html',
                  context=request_context)


def get_all_centres(request):
    from centre_registry.models import Centre
    from django.shortcuts import render
    from django.template import RequestContext

    request_context = RequestContext(request, {'view': 'all_centres',
                                               'all_centres': Centre.objects.all()})

    return render(request,
                  template_name='UI/_all_centres.html',
                  context=request_context)


def get_centre(request, centre_id):
    from centre_registry.models import Centre, URLReference
    from django.shortcuts import get_object_or_404, render
    from django.template import RequestContext

    centre = get_object_or_404(Centre, pk=centre_id)

    request_context = RequestContext(request, {'view': 'centre',
                                               'centre': centre,
                                               'url_references': URLReference.objects.filter(centre__pk=centre.pk)})

    return render(request,
                  template_name='UI/_centre.html',
                  context=request_context)


def get_centres_contacts(request):
    from centre_registry.models import Centre
    from django.shortcuts import render
    from django.template import RequestContext

    request_context = RequestContext(request, {'view': 'centres_contacts',
                                               'all_centres': Centre.objects.all()})

    return render(request,
                  template_name='UI/_centres_contacts.html',
                  context=request_context)


def get_consortia(request):
    from centre_registry.models import Consortium
    from django.shortcuts import render
    from django.template import RequestContext

    request_context = RequestContext(request, {'view': 'consortia',
                                               'consortia': Consortium.objects.all()})

    return render(request,
                  template_name='UI/_consortia.html',
                  context=request_context)

def get_contact(request, contact_id):
    from centre_registry.models import Contact
    from django.shortcuts import get_object_or_404, render
    from django.template import RequestContext

    contact = get_object_or_404(Contact, pk=contact_id)

    request_context = RequestContext(request, {'view': 'contact',
                                               'contact': contact})

    return render(request,
                  template_name='UI/_contact.html',
                  context=request_context)

def get_contacting(request):
    from django.shortcuts import render
    from django.template import RequestContext

    request_context = RequestContext(request, {'view': 'contacting'})

    return render(request,
                  template_name='UI/_contacting.html',
                  context=request_context)


def get_fcs(request):
    from centre_registry.models import FCSEndpoint
    from django.shortcuts import render
    from django.template import RequestContext

    request_context = RequestContext(request, {'view': 'fcs',
                                               'fcs_endpoints': FCSEndpoint.objects.all()})

    return render(request,
                  template_name='UI/_fcs.html',
                  context=request_context)


def get_oai_pmh(request):
    from centre_registry.models import OAIPMHEndpoint
    from django.shortcuts import render
    from django.template import RequestContext

    request_context = RequestContext(request, {'view': 'oai_pmh',
                                               'oai_pmh_endpoints': OAIPMHEndpoint.objects.all()})

    return render(request,
                  template_name='UI/_oai_pmh.html',
                  context=request_context)


def get_map(request):
    from django.shortcuts import render
    from django.template import RequestContext

    request_context = RequestContext(request, {'view': 'map',
                                               'url_prefix': request.build_absolute_uri('/')})

    return render(request,
                  template_name='UI/_map.html',
                  context=request_context)


def get_spf(request):
    from centre_registry.models import SAMLIdentityFederation, SAMLServiceProvider
    from collections import OrderedDict
    from django.shortcuts import render
    from django.template import RequestContext
    from json import loads
    from urllib.request import urlopen

    processed_sps_across_identity_federations = loads(urlopen(
        'https://infra.clarin.eu/aai/sps_at_identity_federations/summary.json').read().decode('utf-8'))

    saml_identity_federations = SAMLIdentityFederation.objects \
        .filter(shorthand__in=processed_sps_across_identity_federations) \
        .extra(select={'shorthand_lower': 'lower(shorthand)'}) \
        .order_by('shorthand_lower') \
        .all()

    identity_federations_intersection_of_centre_registry_and_summary = \
        {saml_identity_federation.shorthand: processed_sps_across_identity_federations[
            saml_identity_federation.shorthand]
         for saml_identity_federation in saml_identity_federations}  # TODO: handle exceptions

    processed_sps_across_identity_federations2 = \
        OrderedDict(sorted(identity_federations_intersection_of_centre_registry_and_summary.items(),
            key=lambda identity_federation_shorthand: identity_federation_shorthand[0].lower()))

    request_context = RequestContext(request, {'view': 'spf',
                                               'saml_service_providers': SAMLServiceProvider.objects.all(),
                                               'saml_identity_federations': saml_identity_federations,
                                               'processed_sps_across_identity_federations': \
                                                   processed_sps_across_identity_federations2})

    return render(request,
                  template_name='UI/_spf.html',
                  context=request_context)