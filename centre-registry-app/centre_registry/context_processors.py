# -*- coding: utf-8 -*-
def tracked_by_piwik(request):
    from django.conf import settings

    if settings.PIWIK_WEBSITE_ID is not None:
        return {'PIWIK_WEBSITE_ID': settings.PIWIK_WEBSITE_ID}
    else:
        return {}


def resource_locations_relative_to_static(request):
    from django.conf import settings

    return {
        'RESOURCE_LOCATION_DATATABLES': settings.RESOURCE_LOCATION_DATATABLES,
        'RESOURCE_LOCATION_CLARIN_STYLE': settings.RESOURCE_LOCATION_CLARIN_STYLE}


def version(request):
    from django.conf import settings

    return {'VERSION': settings.VERSION}