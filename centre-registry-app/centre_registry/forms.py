from django.forms import (CharField, HiddenInput, ModelForm, ModelChoiceField, ModelMultipleChoiceField, Textarea)
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper
from django.contrib.postgres.fields.array import SimpleArrayField # as BaseArrayField

from centre_registry.models import Centre
from centre_registry.models import KCentre
from centre_registry.models import KCentreServiceType
from centre_registry.models import KCentreStatus
from centre_registry.models import ResourceFamily
from centre_registry.models import ShadowCentre
from centre_registry.models import ShadowKCentre
from centre_registry.models import ShadowKCentreServiceType
from centre_registry.models import ShadowKCentreStatus
from centre_registry.models import ShadowOrganisation


from centre_registry.widgets import ArrayFieldInputWidget


# class SimpleArrayField(BaseArrayField):
#     def __int__(self, **kwargs):
#         super().__init__(**kwargs)
#
#     def prepare_value(self, value) -> list:
#         if not isinstance(value, list):
#             return value.split(self.delimiter)
#         return value


class KCentreForm(ModelForm):
    class Meta:
        model = ShadowKCentre
        fields = ["audiences", "competence", "data_types", "generic_topics", "keywords", "language_processing_spec",
                  "linguistic_topics", "modalities", "pid", "tour_de_clarin_interview", "tour_de_clarin_intro",
                  "website_language", "kcentre_fk", "resource_families_fks"]
    #
    kcentre_fk = ModelChoiceField(widget=HiddenInput(), required=False, queryset=Centre.objects.all())
    edit_author_name = CharField()
    template_name = "forms/_edit_form_snippet.html"
    audiences = SimpleArrayField(CharField(),
                                 label="Audience",
                                 widget=ArrayFieldInputWidget())
    competence = CharField(widget=Textarea())
    data_types = SimpleArrayField(CharField(),
                                  label="Data types",
                                  widget=ArrayFieldInputWidget())
    generic_topics = SimpleArrayField(CharField(),
                                      label="Generic topics",
                                      widget=ArrayFieldInputWidget())
    keywords = SimpleArrayField(CharField(),
                                label="Keywords",
                                widget=ArrayFieldInputWidget())
    language_processing_spec = SimpleArrayField(CharField(),
                                                label="Language processing specification",
                                                widget=ArrayFieldInputWidget())
    modalities = SimpleArrayField(CharField(),
                                  label="Modalities")
    pid = CharField(label="Certificate PID")


    # FK's
    shadow_centre_fk = ModelChoiceField(queryset=ShadowCentre.objects.all(), label="Centre", required=True)
    shadow_secondary_hosts_fks = ModelMultipleChoiceField(queryset=ShadowOrganisation.objects.all(),
                                                          label="Secondary host",
                                                          required=False,
                                                          widget=RelatedFieldWidgetWrapper(
                                                              widget=FilteredSelectMultiple('Organisation',
                                                                                            False),
                                                              rel=ShadowKCentre.shadow_secondary_hosts_fks.rel,
                                                              admin_site=admin.site))
    shadow_service_type_fks = ModelMultipleChoiceField(queryset=ShadowKCentreServiceType.objects.all(),
                                                       label="Service type",
                                                       required=False,
                                                       widget=RelatedFieldWidgetWrapper(
                                                           widget=FilteredSelectMultiple('Service Type',
                                                                                         False),
                                                           rel=ShadowKCentre.shadow_kcentre_service_type_fks.rel,
                                                           admin_site=admin.site))
    shadow_kcentre_status_fk = ModelChoiceField(queryset=KCentreStatus.objects.all(), label="Status", required=False)
