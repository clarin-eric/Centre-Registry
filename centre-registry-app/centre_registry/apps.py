# from django.contrib.admin.apps import AdminConfig
from django.apps import AppConfig

import centre_registry


class CentreRegistryConfig(AppConfig):
    name = centre_registry.__name__
    verbose_name = 'Centre Registry'


# class CentreRegistryAdminConfig(AdminConfig):
#     default_site = "centre_registry.admin.CentreRegistryAdminSite"
