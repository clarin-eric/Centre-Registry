from django.conf import settings


def tracked_by_piwik(request):
    # pylint: disable=unused-argument
    if settings.PIWIK_WEBSITE_ID is not None:
        return {'PIWIK_WEBSITE_ID': settings.PIWIK_WEBSITE_ID}
    else:
        return {}


def version(request):
    # pylint: disable=unused-argument
    return {'VERSION': settings.VERSION}


def centre_profile_xsd_url(request):
    return {'CENTRE_PROFILE_XSD_URL': settings.CENTRE_REGISTRY_XSD_URL}


def google_api_key(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}

