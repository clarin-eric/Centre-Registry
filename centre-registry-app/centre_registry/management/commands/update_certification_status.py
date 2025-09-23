from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.utils import timezone
from django.test.client import RequestFactory
from django.utils.timezone import localdate

import logging

from centre_registry.models import Centre, CertificationStatus


DEFAULT_EMAIL = settings.DEFAULT_FROM_EMAIL

class Command(BaseCommand):
    help = 'Command to update certification status based on expiration date'

    def handle(self, *args, **options):
        today_date = timezone.now().date()

        centres = Centre.objects.all()
        expired_status_id = CertificationStatus.objects.get(status="Pending (recertification)")
        certified_status_id = CertificationStatus.objects.get(status="Certified")
        outdated_centres = []

        for centre in centres:
            type_certification_statuses = centre.type_certification_status_fk.all()
            for type_certification_status in type_certification_statuses:
                assessment_date = type_certification_status.assessmentdate
                due_date = assessment_date.duedate
                if due_date < today_date and type_certification_status.certification_status == certified_status_id:
                    type_certification_status.certification_status = expired_status_id
                    type_certification_status.assessmentdate = assessment_date
                    type_certification_status.type_status_comment = ''
                    type_certification_status.save()

                    centre.requires_manual_certificate_validation = True
                    outdated_centres.append(centre.name)
                    centre.save()

        if outdated_centres:
            outdated_centres = '\n'.join(outdated_centres)
            subject = "Centres certification expired"
            message = "Following centre has their assessment dates expired today:" + outdated_centres

            send_mail(subject=subject,
                      message=message,
                      from_email='michal@clarin.eu',
                      recipient_list=['michal@clarin.eu'],
                      fail_silently=False
                      )
