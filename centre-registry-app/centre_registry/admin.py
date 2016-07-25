from centre_registry.models import Centre
from centre_registry.models import CentreType
from centre_registry.models import Consortium
from centre_registry.models import Contact
from centre_registry.models import FCSEndpoint
from centre_registry.models import MetadataFormat
from centre_registry.models import OAIPMHEndpoint
from centre_registry.models import SAMLIdentityFederation
from centre_registry.models import SAMLServiceProvider
from centre_registry.models import URLReference
from django.contrib import admin

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
