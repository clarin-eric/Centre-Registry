from django.db import migrations

from centre_registry.models import CertificationStatus
from centre_registry.models import Centre

def forwards(apps, schema_editor):
    # CentreModel and OrganisationModel are classes, therefore CamelCase
    centres = Centre.objects.all()

    if not CertificationStatus.objects.filter(status='Certified').exists():
        CERTIFIED = CertificationStatus(status='Certified')
        CERTIFIED.save()
    else:
        CERTIFIED = CertificationStatus.objects.get(status='Certified')

    if not CertificationStatus.objects.filter(status='Pending').exists():
        PENDING = CertificationStatus(status='Pending')
        PENDING.save()
    else:
        PENDING = CertificationStatus.objects.get(status='Pending')

    if not CertificationStatus.objects.filter(status='Pending (recertification)').exists():
        PENDING_RECERTIFICATION = CertificationStatus(status='Pending (recertification)')
        PENDING_RECERTIFICATION.save()
    else:
        PENDING_RECERTIFICATION = CertificationStatus.objects.get(status='Pending (recertification)')

    if not CertificationStatus.objects.filter(status='Suspended').exists():
        SUSPENDED = CertificationStatus(status='Suspended')
        SUSPENDED.save()
    else:
        SUSPENDED = CertificationStatus.objects.get(status='Suspended')

    if not CertificationStatus.objects.filter(status='Archived').exists():
        ARCHIVED = CertificationStatus(status='Archived')
        ARCHIVED.save()
    else:
        ARCHIVED = CertificationStatus(status='Archived')

    for centre in centres:
        status_comment = centre.type_status_comment
        if status_comment == 'Certified':
            centre.type_certification_status = CERTIFIED
        elif "expired" in status_comment:
            centre.type_certification_status = PENDING_RECERTIFICATION


class Migration(migrations.Migration):
    dependencies = [
        ('centre_registry', '0041_certificationstatus_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards)
    ]
