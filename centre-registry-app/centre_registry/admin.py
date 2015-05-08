# -*- coding: utf-8 -*-

from django.contrib import admin

from centre_registry.models import Centre, CentreType, Consortium, Contact, FCSEndpoint, \
    MetadataFormat, OAIPMHEndpoint, SAMLServiceProvider, SAMLIdentityFederation, URLReference

admin.site.site_header = "Centre Registry administration"
admin.site.app_name = "Centre Registry"
admin.site.register(Centre)
admin.site.register(CentreType)
admin.site.register(Consortium)
admin.site.register(Contact)
admin.site.register(FCSEndpoint)
admin.site.register(MetadataFormat)
admin.site.register(OAIPMHEndpoint)
admin.site.register(SAMLServiceProvider)
admin.site.register(SAMLIdentityFederation)
admin.site.register(URLReference)
