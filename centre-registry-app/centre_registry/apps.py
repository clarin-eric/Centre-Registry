from django.contrib.admin import apps
from django.apps import AppConfig

import centre_registry


class CentreRegistryConfig(AppConfig):
    name = centre_registry.__name__
    verbose_name = 'Centre Registry'
