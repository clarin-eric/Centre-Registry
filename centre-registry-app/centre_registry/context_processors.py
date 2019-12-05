from django.conf import settings


def tracked_by_piwik(request):
    # pylint: disable=unused-argument
    if settings.PIWIK_WEBSITE_ID is not None:
        return {'PIWIK_WEBSITE_ID': settings.PIWIK_WEBSITE_ID}
    else:
        return {}


def res_locs_relv_to_static(request):
    # pylint: disable=unused-argument
    if settings.RESOURCE_LOCATION_DATATABLES is not None and settings.RESOURCE_LOCATION_CLARIN_STYLE is not None:
        return {
            'RESOURCE_LOCATION_DATATABLES': settings.RESOURCE_LOCATION_DATATABLES,
            'RESOURCE_LOCATION_CLARIN_STYLE':
            settings.RESOURCE_LOCATION_CLARIN_STYLE
        }
        return {}


def version(request):
    # pylint: disable=unused-argument
    return {'VERSION': settings.VERSION}
