from django.db import migrations

from centre_registry.models import CertificationStatus
from centre_registry.models import Centre

def forwards(apps, schema_editor):
    # CentreModel and OrganisationModel are classes, therefore CamelCase
    centres = Centre.objects.all()

    stat = CertificationStatus.objects.all()
    print(stat)
    for s in stat:
        print(s.status)
    CERTIFIED = CertificationStatus.objects.get(status='Certified')
    print(CERTIFIED.status)
    PENDING = CertificationStatus.objects.get(status='Pending')
    PENDING_RECERTIFICATION = CertificationStatus.objects.get(status='Pending (recertification)')
    print(PENDING_RECERTIFICATION)
    SUSPENDED = CertificationStatus.objects.get(status='Suspended')
    ARCHIVED = CertificationStatus.objects.get(status='Archived')

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
