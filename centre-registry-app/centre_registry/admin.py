from centre_registry.models import AssessmentDates
from centre_registry.models import Centre
from centre_registry.models import CentreType
from centre_registry.models import Consortium
from centre_registry.models import Contact
from centre_registry.models import KCentre
from centre_registry.models import KCentreFormModel
from centre_registry.models import KCentreServiceType
from centre_registry.models import KCentreStatus
from centre_registry.models import FCSEndpoint
from centre_registry.models import OAIPMHEndpoint
from centre_registry.models import OAIPMHEndpointSet
from centre_registry.models import Organisation
from centre_registry.models import OrganisationForm
from centre_registry.models import ResourceFamily
from centre_registry.models import SAMLIdentityFederation
from centre_registry.models import SAMLServiceProvider
from centre_registry.models import URLReference

from django.contrib import admin


# class CentreRegistryAdminSite(admin.AdminSite):
#     def get_app_list(self, request):
#         app_list = super().get_app_list(request)
#         app_list += [
#             {
#                 "name": "KCentre Edit Form Moderation",
#                 "app_label": "centre_registry",
#                 # "app_url": "/admin/test_view",
#                 "models": [
#                     {
#                         "name": "Centre Registry",
#                         "object_name": "centre_registry_edit_form",
#                         "admin_url": "/admin/kcentre_form_moderation/",
#                         "view_only": True,
#                     }
#                 ],
#             }
#         ]
#         return app_list


class OrphanContactFilter(admin.SimpleListFilter):
    title = 'contact type'
    parameter_name = 'contact_assignment'

    def lookups(self, request, model_admin):
        return [
                ('administrative_contacts', 'Administrative contacts'),
                ('monitoring_contacts', 'Monitoring contacts'),
                ('technical_contacts', 'Technical contacts'),
                ('orphan_contacts', 'Orphan contacts'),
                ]

    def queryset(self, request, queryset):
        if self.value() == 'orphan_contacts':
            contacts = Contact.objects.values('id')
            orphan_contacts = Contact.objects.exclude(
                administrative_contact__in=contacts).exclude(
                monitoring_contacts__in=contacts).exclude(
                technical_contact__in=contacts)
            return orphan_contacts

        if self.value() == 'administrative_contacts':
            contacts = Contact.objects.values('id')
            administrative_contacts = Contact.objects.filter(administrative_contact__in=contacts).distinct()
            return administrative_contacts

        if self.value() == 'monitoring_contacts':
            contacts = Contact.objects.values('id')
            monitoring_contacts = Contact.objects.filter(monitoring_contacts__in=contacts).distinct()
            return monitoring_contacts

        if self.value() == 'technical_contacts':
            contacts = Contact.objects.values('id')
            technical_contacts = Contact.objects.filter(technical_contact__in=contacts).distinct()
            return technical_contacts


class ContactAdmin(admin.ModelAdmin):
    list_filter = (OrphanContactFilter, )


class OAIPMHEndpointSpecInLine(admin.TabularInline):
    extra = 0
    verbose_name = "OAI-PMH Set"
    verbose_name_plural = "OAI-PMH Sets"
    model = OAIPMHEndpoint.oai_pmh_sets.through


class OAIPMHEndpointAdmin(admin.ModelAdmin):
    inlines = [OAIPMHEndpointSpecInLine]
    exclude = ["oai_pmh_sets"]


class AssessmentDateInline(admin.StackedInline):
    extra = 0
    verbose_name = "Centre assessment date"
    verbose_name_plural = "Centre assessment dates"
    model = Centre.assessmentdates.through


class CentreAdmin(admin.ModelAdmin):
    inlines = [AssessmentDateInline]
    exclude = ["assessmentdates"]


class AssessmentDateAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Hide model from index
        """
        return {}


# class KCentreCentreInline(admin.ModelAdmin):
#     form = CentreInlineFormSet


admin.site.site_header = "Centre Registry administration"
admin.site.app_name = "Centre Registry"


admin.site.register(AssessmentDates, AssessmentDateAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Centre, CentreAdmin)
admin.site.register(CentreType)
admin.site.register(Consortium)
admin.site.register(KCentre)
admin.site.register(KCentreFormModel)
admin.site.register(KCentreServiceType)
admin.site.register(KCentreStatus)
admin.site.register(FCSEndpoint)
admin.site.register(Organisation)
admin.site.register(OrganisationForm)
admin.site.register(OAIPMHEndpoint, OAIPMHEndpointAdmin)
admin.site.register(OAIPMHEndpointSet)
admin.site.register(ResourceFamily)
admin.site.register(SAMLServiceProvider)
admin.site.register(SAMLIdentityFederation)
admin.site.register(URLReference)
