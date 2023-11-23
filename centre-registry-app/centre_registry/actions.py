from django.contrib import admin
from django.forms.models import model_to_dict


from centre_registry.models import Centre
from centre_registry.models import KCentre
from centre_registry.models import KCentreServiceType
from centre_registry.models import KCentreStatus
from centre_registry.models import Organisation
from centre_registry.models import ShadowCentre
from centre_registry.models import ShadowKCentre
from centre_registry.models import ShadowKCentreServiceType
from centre_registry.models import ShadowKCentreStatus
from centre_registry.models import ShadowOrganisation
from centre_registry.utils import materialise_shadow, materialise_shadows


@admin.action(description="Accept selected KCentre")
# TODO type hinting
def publish_kcentres(modeladmin, request, queryset):
    # TODO that has to be terribly slow, each __in requires JOIN
    for shadow_kcentre in queryset:
        if not isinstance(shadow_kcentre, ShadowKCentre):
            raise TypeError(f"Expected {ShadowKCentre} instance, got {type(shadow_kcentre)}")

        publish_kcentre(shadow_kcentre)


def publish_kcentre(shadow_kcentre):
    shadow_centre = shadow_kcentre.shadow_centre_fk
    shadow_kcentre_service_types = shadow_kcentre.shadow_kcentre_service_type_fks
    shadow_kcentre_status = shadow_kcentre.shadow_kcentre_status_fk
    shadow_secondary_hosts = shadow_kcentre.shadow_secondary_host_fk

    # if request for new KCentre
    if shadow_kcentre.kcentre_fk is None:
        kcentre = materialise_shadow(shadow_kcentre, KCentre)
    # else edit existing KCentre
    else:
        kcentre = KCentre.objects.get(pk=shadow_kcentre.kcentre_fk)
        shadow_kcentre_dict = model_to_dict(shadow_kcentre)
        kcentre.objects.update(**shadow_kcentre_dict)

    # relations have to be preserved
    # KCentre 1---1 Centre 1---1 Organisation
    centre = kcentre.centre_fk
    if not centre:
        centre = materialise_shadow(shadow_centre, Centre)
    organisation = centre.organisation_fk

    shadow_centre_dict = model_to_dict(shadow_centre)
    shadow_organisation_dict = model_to_dict(shadow_centre.shadow_organisation_fk)

    organisation.objects.update(**shadow_organisation_dict).save()
    centre.objects.update(**shadow_centre_dict).save()

    centre.organisation_fk = organisation
    kcentre.centre_fk = centre

    secondary_hosts = Organisation.objects.none()
    if shadow_secondary_hosts:
        for shadow_secondary_host in shadow_secondary_hosts:
            # modify existing organisation
            if shadow_secondary_host.organisation_fk:
                organisation = Organisation.objects.get(pk=shadow_secondary_host.organisation_fk)
                shadow_secondary_host_dict = model_to_dict(shadow_secondary_host)
                organisation.objects.update(**shadow_secondary_host_dict)
            # create new organisation from its shadow
            else:
                organisation = materialise_shadow(shadow_secondary_host, Organisation)
            secondary_hosts |= organisation

    kcentre_service_types = materialise_shadows(shadow_kcentre_service_types, KCentreServiceType).save()
    kcentre_status = materialise_shadow(shadow_kcentre_status, KCentreStatus).save()

    kcentre.service_type_fks = kcentre_service_types
    kcentre.status_fk = kcentre_status

    kcentre.save()