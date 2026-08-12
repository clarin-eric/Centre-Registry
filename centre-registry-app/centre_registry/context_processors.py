from django.conf import settings


import re

def tracked_by_piwik(request):
    # pylint: disable=unused-argument
    if settings.PIWIK_WEBSITE_ID is not None:
        return {'PIWIK_WEBSITE_ID': settings.PIWIK_WEBSITE_ID}
    else:
        return {}


def version(request):
    # pylint: disable=unused-argument
    version = settings.VERSION
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(version)
    alpha_regex = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(-)?a[0-9]+$")
    beta_regex = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(-)?(b|rc)[0-9]+$")
    production_regex = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
    print("###################################################################")
    if alpha_regex.match(version):
        print("1")
        return {"VERSION": version, "INSTANCE": "ALPHA"}
    elif beta_regex.match(version):
        print("2")
        return {'VERSION': version, "INSTANCE": "BETA"}
    elif production_regex.match(version):
        print("3")
        return {'VERSION': version, "INSTANCE": ""}


def centre_profile_xsd_url(request):
    return {'CENTRE_PROFILE_XSD_URL': settings.CENTRE_REGISTRY_XSD_URL}


def google_api_key(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}
