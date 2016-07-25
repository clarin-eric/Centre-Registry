import centre_registry
from django.apps import AppConfig


class CentreRegistryConfig(AppConfig):
    name = centre_registry.__name__
    verbose_name = 'Centre Registry'
