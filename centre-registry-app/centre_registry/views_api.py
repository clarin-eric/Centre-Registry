from inspect import getmembers as inspect_getmembers
from inspect import isclass as inspect_isclass
from json import loads as json_loads

from centre_registry import models
from centre_registry.models import Centre
from centre_registry.models import FCSEndpoint
from centre_registry.models import OAIPMHEndpointSet
from centre_registry.models import URLReference
from django.core import serializers
from django.core.exceptions import ViewDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import render_to_string


def get_centre(request, centre_id):
    """API v1"""
    centre = get_object_or_404(Centre, pk=centre_id)
    request_context = RequestContext(
        request,
        {'centre': centre,
         'oai_pmh_endpoints':
         [oai_pmh_endpoint for oai_pmh_endpoint in [
             endpoint_set.oaipmh_endpoints for endpoint_set in OAIPMHEndpointSet.objects.filter(centre__pk=centre.pk)]],
         'fcs_endpoints': FCSEndpoint.objects.filter(centre__pk=centre.pk),
         'url_references': URLReference.objects.filter(centre__pk=centre.pk),
         'url_prefix': request.build_absolute_uri('/')})
    return render(
        request,
        template_name='API/centre.xml',
        # Djnago 1.11+ requires context in form of dict, flatten() returns RequestContext as dict
        context=request_context.flatten(),
        content_type='application/xml')


def get_all_centres(request):
    """API v1"""
    request_context = RequestContext(
        request, {'all_centres': Centre.objects.all(),
                  'url_prefix': request.build_absolute_uri('/').replace('http://', 'https://')})
    return render(
        request,
        template_name='API/all_centres.xml',
        # Djnago 1.11+ requires context in form of dict, flatten() returns RequestContext as dict
        context=request_context.flatten(),
        content_type='application/xml')


def _get_model(model_name):
    model_names = inspect_getmembers(models, inspect_isclass)
    for (imported_model_name, class_object) in model_names:
        if imported_model_name == model_name:
            return json_loads(
                serializers.serialize('json', class_object.objects.all()))
    else:
        raise ViewDoesNotExist(model_name)


def get_model(request, model):
    # pylint: disable=unused-argument
    return JsonResponse(_get_model(model_name=model), safe=False)


def get_centres_kml(request, types):
    # Whitelist of the allowed types
    if types == '':
        types = 'ABCDETK'
    types_list = set(types)  # TODO: refactor
    types_list_iter = iter(types_list)  # TODO: refactor

    type_query = Q(type__type=next(types_list_iter))
    for a_type in types_list_iter:
        type_query = type_query.__or__(Q(type__type=a_type))

    request_context = RequestContext(
        request, {'centres':
                  models.Centre.objects.filter(type_query).distinct(),
                  'types': sorted(types_list),
                  'url_prefix': request.build_absolute_uri('/').replace('http://', 'https://')})
    return render(
        request,
        template_name='API/centres_map.kml',
        # Djnago 1.11+ requires context in form of dict, flatten() returns RequestContext as dict
        context=request_context.flatten(),
        content_type='application/vnd.google-earth.kml+xml')
