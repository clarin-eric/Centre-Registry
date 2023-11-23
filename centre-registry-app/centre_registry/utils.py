"""
Utility functions
"""

from django.shortcuts import _get_queryset
from django.forms.models import model_to_dict
from typing import Callable, Iterable

# Production models
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
from centre_registry.models import ShadowOrganisation

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


def materialise_shadow(shadow_object: object, model_class: Callable[[dict], Model]):
    model_dict = model_to_dict(shadow_object)
    return model_class.objects.create(**model_dict)


def materialise_shadows(shadow_objects: Iterable[object], model_class: Callable[[dict], Model]):
    queryset = model_class.objects.none()
    for shadow_object in shadow_objects:
        # queryset merge operator
        queryset |= materialise_shadow(shadow_object, model_class)
    return queryset


def populate_shadow_tables():
    organisations = Organisation.objects.all()
    for organisation in organisations:
        shadow_organisation = ShadowOrganisation(fk_organisation=organisation, **model_to_dict(organisation))
        shadow_organisation.save()
    centres = Centre.objects.all()
    for centre in centres:
        ShadowOrganisation.filter(fk_organisation__pk=centre.organisation_name)
        shadow_centre = ShadowCentre.objects.create(fk_centre=centre, **model_to_dict(centre))
