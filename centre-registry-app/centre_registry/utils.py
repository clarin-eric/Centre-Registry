"""
Utility functions
"""

from django.shortcuts import _get_queryset
from typing import Callable, Iterable
from django.forms.models import model_to_dict

# Production models
from centre_registry.models import Centre
from centre_registry.models import Contact
from centre_registry.models import KCentre
from centre_registry.models import KCentreServiceType
from centre_registry.models import KCentreStatus
from centre_registry.models import Model
from centre_registry.models import Organisation

# Shadow models storing edit requests for moderation
from centre_registry.models import ShadowCentre
from centre_registry.models import ShadowContact
from centre_registry.models import ShadowKCentre
from centre_registry.models import ShadowKCentreServiceType
from centre_registry.models import ShadowKCentreStatus
from centre_registry.models import ShadowOrganisation


import logging

logger = logging.getLogger(__name__)


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
# SOURCE:
# https://stackoverflow.com/questions/62840397/how-to-pass-foreignkey-in-dict-to-create-model-object-django#
#
#
# modified model_to_dict returning fk's instances instead of id's,
# allowing SomeModel.objects.create(**model_to_dict_wfk(some_instance)
# extended to support exclude for fk's
def model_to_dict_wfk(modelobj, *args, **kwargs):
    opts = modelobj._meta.fields
    exclude = {}
    if 'exclude' in kwargs.keys():
        exclude = set(kwargs['exclude'])
    modeldict = model_to_dict(modelobj, *args, **kwargs)
    for m in opts:
        if m.is_relation:
            foreignkey = getattr(modelobj, m.name)
            if foreignkey and m.name not in exclude:
                try:
                    modeldict[m.name] = foreignkey
                except:
                    pass
    return modeldict
################################################################################


def materialise_shadow(shadow_object: object, model_class: Callable[[dict], Model]):
    """
        Function creates production instance from shadow after moderation
    """
    model_dict = model_to_dict_wfk(shadow_object)
    return model_class.objects.create(**model_dict)


def materialise_shadows(shadow_objects: Iterable[object], model_class: Callable[[dict], Model]):
    """
        Maps utils.materialise_shadow() over iterable
    """
    queryset = model_class.objects.none()
    for shadow_object in shadow_objects:
        # queryset merge operator
        queryset |= materialise_shadow(shadow_object, model_class)
    return queryset


def clean_shadow_tables():
    # Remove all records from shadow tables
    ShadowOrganisation.objects.all().delete()
    ShadowCentre.objects.all().delete()
    ShadowKCentreServiceType.objects.all().delete()
    ShadowKCentreStatus.objects.all().delete()
    ShadowKCentre.objects.all().delete()


def populate_shadow_tables():
    """
    Create shadow copies of instances in production database
    """
    # Clean existing shadow artifacts:
    logger.critical("NIEDZIAŁA")
    clean_shadow_tables()

    logger.critical("DZIAŁA")
    # Organisation
    organisations = Organisation.objects.all()
    for organisation in organisations:
        ShadowOrganisation.objects.create(organisation_fk=organisation, **model_to_dict_wfk(organisation))
    centres = Centre.objects.all()

    contacts = Contact.objects.all()
    for contact in contacts:
        ShadowContact.objects.get_or_create(contact_fk=contact, **model_to_dict(contact))

    # Centres
    for centre in centres:
        logger.critical("centres")
        organisation = centre.organisation_fk

        administrative_contact = centre.administrative_contact
        monitoring_contacts = centre.monitoring_contacts
        technical_contact = centre.technical_contact

        logger.critical("centres1")
        shadow_administrative_contact = administrative_contact.shadow_contact
        shadow_monitoring_contacts = [monitoring_contact.shadow_contact.get() for monitoring_contact in monitoring_contacts.all()]
        logger.critical("centres2")
        shadow_organisation = organisation.shadow_organisation
        logger.critical("centres3")
        shadow_technical_contact = technical_contact.shadow_contact
        logger.critical(model_to_dict_wfk(centre, exclude=['type',
                                                             'organisation_fk',
                                                             'administrative_contact',
                                                             'monitoring_contacts',
                                                             'technical_contact',
                                                             'assessmentdates']))
        shadow_centre = ShadowCentre.objects.create(centre_fk=centre,
                                                    shadow_organisation_fk=shadow_organisation.get(),
                                                    **model_to_dict_wfk(centre,
                                                                        exclude=['type',
                                                                                 'organisation_fk',
                                                                                 'administrative_contact',
                                                                                 'monitoring_contacts',
                                                                                 'technical_contact',
                                                                                 'assessmentdates']))
        logger.critical("centres4")
        logger.critical(f'{centre.assessmentdates.all()}')
        shadow_centre.assessmentdates.set(centre.assessmentdates.all())
        logger.critical("centres5")
        shadow_centre.shadow_administrative_contact_fk = shadow_administrative_contact.get()
        logger.critical("centres6")
        shadow_centre.shadow_monitoring_contacts_fks.set(shadow_monitoring_contacts)
        logger.critical("centres7")
        shadow_centre.shadow_technical_contact = shadow_technical_contact.get()
        logger.critical("centres8")
        shadow_centre.type.set(centre.type.all())
        logger.critical("centres9")
        shadow_centre.save()

    # Service types
    service_types = KCentreServiceType.objects.all()
    for service_type in service_types:
        ShadowKCentreServiceType.objects.create(service_type_fk=service_type, **model_to_dict_wfk(service_type))

    # KCentre statuses
    kcentre_statuses = KCentreStatus.objects.all()
    for kcentre_status in kcentre_statuses:
        ShadowKCentreStatus.objects.create(status_fk=kcentre_status, **model_to_dict_wfk(kcentre_status))

    logger.critical("Went far")
    # KCentre
    kcentres = KCentre.objects.all()
    for kcentre in kcentres:
        # find all shadows of related instances
        related_centre = kcentre.centre_fk
        logger.critical(related_centre)
        related_centre_shadow = related_centre

        related_service_types = kcentre.service_type_fks
        related_service_types_shadow = related_service_types.self_shadow.all()

        related_status = kcentre.status_fk
        logging.critical("here")
        related_status_shadow = related_status.self_shadow.all().first()
        logging.critical('or here')
        related_secondary_hosts = kcentre.secondary_hosts_fks
        related_secondary_hosts_shadow = {related_secondary_host.self_shadow.all().first()
                                          for related_secondary_host in related_secondary_hosts}
        logging.critical('and_here')

        kcentre_dict = model_to_dict_wfk(kcentre)
        kcentre_dict["shadow_centre_fk"] = related_centre_shadow
        kcentre_dict["shadow_kcentre_status_fk"] = related_status_shadow

        shadow_kcentre = ShadowKCentre.objects.create(kcentre_ptr_id=kcentre, **kcentre_dict)
        for related_secondary_host in related_secondary_hosts_shadow:
            shadow_kcentre.secondary_hosts_fks.add(related_secondary_host)

        for related_service_type in related_service_types_shadow:
            shadow_kcentre.service_type_fks.add(related_service_type)

        shadow_kcentre.save()
