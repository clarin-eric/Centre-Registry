"""
Utility functions
"""

from django.shortcuts import _get_queryset
from django.forms.models import model_to_dict

# Production models with not moderated Shadows
from centre_registry.models import Centre
from centre_registry.models import KCentre
from centre_registry.models import KCentreServiceType
from centre_registry.models import KCentreStatus
from centre_registry.models import Model
from centre_registry.models import ResourceFamily
from centre_registry.models import Organisation

# Shadow models storing edit requests for moderation
from centre_registry.models import ShadowCentre
from centre_registry.models import ShadowKCentre
from centre_registry.models import ShadowKCentreServiceType
from centre_registry.models import ShadowKCentreStatus
from centre_registry.models import ShadowResourceFamily
from centre_registry.models import ShadowOrganisation


MODEL_SHADOW_PAIRS = [
    (Organisation, ShadowOrganisation),
    (Centre, ShadowCentre),
    (KCentreServiceType, ShadowKCentreServiceType),
    (KCentreStatus, ShadowKCentreStatus),
    (ResourceFamily, ShadowResourceFamily),
    (KCentre, ShadowKCentre),
]

################################################################################
# SOURCE:
# https://github.com/skorokithakis/django-annoying
#
# Copypaste to avoid installing entire dependency in the container
def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
################################################################################


def drop_shadow_tables_data():
    for _, shadow_model in MODEL_SHADOW_PAIRS:
        shadow_model.objects.all().delete()


def populate_shadow_tables_data():
    organisations = Organisation.objects.all()
    for organisation in organisations:
        shadow_organisation = ShadowOrganisation(fk_organisation=organisation, **model_to_dict(organisation))
        shadow_organisation.save()
    centres = Centre.objects.all()
    for centre in centres:
        ShadowOrganisation.filter(fk_organisation__pk=centre.organisation_name)
        shadow_centre = ShadowCentre(fk_centre=centre, **model_to_dict(centre))

