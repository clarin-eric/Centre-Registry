# -*- coding: utf-8 -*-

## API v1

def get_centre(request, centre_id):
    from centre_registry.models import Centre, FCSEndpoint, OAIPMHEndpoint, URLReference
    from django.shortcuts import get_object_or_404, render
    from django.template import RequestContext

    centre = get_object_or_404(Centre, pk=centre_id)

    request_context = RequestContext(request, {'centre': centre,
                                               'oai_pmh_endpoints': OAIPMHEndpoint.objects.filter(centre__pk=centre.pk),
                                               'fcs_endpoints': FCSEndpoint.objects.filter(centre__pk=centre.pk),
                                               'url_references': URLReference.objects.filter(centre__pk=centre.pk),
                                               'url_prefix': request.build_absolute_uri('/')})

    return render(request,
                  template_name='API/centre.xml',
                  context=request_context,
                  content_type='application/xml')


def get_all_centres(request):
    from centre_registry.models import Centre
    from django.shortcuts import render
    from django.template import RequestContext

    request_context = RequestContext(request, {'all_centres': Centre.objects.all(),
                                               'url_prefix': request.build_absolute_uri('/')})

    return render(request,
                  template_name='API/all_centres.xml',
                  context=request_context,
                  content_type='application/xml')


## API v2

def _get_model(model_name):
    from centre_registry import models
    from inspect import getmembers as inspect_getmembers, isclass as inspect_isclass

    model_names = inspect_getmembers(models, inspect_isclass)

    for (imported_model_name, class_object) in model_names:
        if imported_model_name == model_name:
            from json import loads as json_loads
            from django.core import serializers

            return json_loads(serializers.serialize('json', class_object.objects.all()))
    else:
        from django.core.exceptions import ViewDoesNotExist

        raise ViewDoesNotExist(model_name)


def get_model(request, model):
    from django.http import JsonResponse

    return JsonResponse(_get_model(model_name=model), safe=False)


def get_centres_kml(request, types):
    from centre_registry import models
    from django.shortcuts import render
    from django.db.models import Q
    from django.template import RequestContext

    ## Whitelist of the allowed types
    if types == '':
        types = 'ABCDET'
    types_list = set(types)  # TODO: refactor
    types_list_iter = iter(types_list)  # TODO: refactor

    # print(models.CentreType.objects.distinct()) # TODO: DEBUG

    type_query = Q(type__type=next(types_list_iter))
    for a_type in types_list_iter:
        type_query = type_query.__or__(Q(type__type=a_type))

    request_context = RequestContext(request, {'centres': models.Centre.objects.filter(type_query).distinct(),
                                               'types': sorted(types_list),
                                               'url_prefix': request.build_absolute_uri('/')})

    return render(request,
                  template_name='API/centres_map.kml',
                  context=request_context,
                  content_type='application/vnd.google-earth.kml+xml')