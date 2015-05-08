# -*- coding: utf-8 -*-

from django.apps import AppConfig

import centre_registry


class CentreRegistryConfig(AppConfig):
    name = centre_registry.__name__
    verbose_name = 'Centre Registry'
