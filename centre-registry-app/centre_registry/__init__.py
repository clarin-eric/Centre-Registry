# -*- coding: utf-8 -*-

__all__ = ['admin', 'apps', 'context_processors', 'models', 'test_api', 'test_ui', 'views_ui', 'views_api']

import centre_registry.apps

default_app_config = '{0}.{1}'.format(centre_registry.apps.__name__,
                                      centre_registry.apps.CentreRegistryConfig.__qualname__)
