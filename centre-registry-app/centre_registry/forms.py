from django.forms import (CharField, HiddenInput, ModelForm, ModelChoiceField, ModelMultipleChoiceField,
                          URLField, Textarea)
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple, RelatedFieldWidgetWrapper
from django.contrib.postgres.fields.array import SimpleArrayField # as BaseArrayField

from .models import Centre, KCentre, KCentreFormModel, ResourceFamily, Organisation, KCentreServiceType, KCentreStatus
from .widgets import ArrayFieldInputWidget


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
        model = KCentreFormModel
        fields = ["audiences", "competence", "data_types", "generic_topics", "keywords", "language_processing_spec",
                  "linguistic_topics", "modalities", "pid", "tour_de_clarin_interview", "tour_de_clarin_intro",
                  "website_language", "centre_fk", "kcentre_fk", "resource_families_fks"]
        widgets = {'kcentre_fk': HiddenInput()}
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
    centre_fk = ModelChoiceField(queryset=Centre.objects.all(), label="Centre", required=False)
    kcentre_fk = ModelChoiceField(queryset=KCentre.objects.all(), label="KCentre", required=False)
    resource_families_fks = ModelMultipleChoiceField(queryset=ResourceFamily.objects.all(), label="Resource families",
                                                     required=False)
    secondary_hosts_fks = ModelMultipleChoiceField(queryset=Organisation.objects.all(), label="Secondary host",
                                                   required=False,
                                                   widget=RelatedFieldWidgetWrapper(
                                                       widget=FilteredSelectMultiple('Organisation',
                                                                                     False),
                                                       rel=KCentreFormModel.secondary_hosts_fks.rel,
                                                       admin_site=admin.site))
    service_type_fk = ModelMultipleChoiceField(queryset=KCentreServiceType.objects.all(), label="Service type",
                                               required=False,
                                               widget=RelatedFieldWidgetWrapper(
                                                   widget=FilteredSelectMultiple('Service Type',
                                                                                 False),
                                                   rel=KCentreFormModel.service_type_fks.rel,
                                                   admin_site=admin.site))
    status_fk = ModelChoiceField(queryset=KCentreStatus.objects.all(), label="Status", required=False)
