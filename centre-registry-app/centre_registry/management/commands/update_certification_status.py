from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.utils import timezone
from django.test.client import RequestFactory
from django.utils.timezone import localdate

import logging

from centre_registry.models import Centre, CertificationStatus
from centre_registry.context_processors import version


class Command(BaseCommand):
    help = 'Command to update certification status based on expiration date'

    def handle(self, *args, **options):
        today_date = timezone.now().date()

        centres = Centre.objects.all()
        expired_status_id = CertificationStatus.objects.get(status="Pending (recertification)")
        certified_status_id = CertificationStatus.objects.get(status="Certified")
        outdated_centres = []

        for centre in centres:
            type_certification_statuses = centre.type_certification_status_fks.all()
            for type_certification_status in type_certification_statuses:
                assessment_date = type_certification_status.assessmentdate
                due_date = assessment_date.duedate
                if due_date < today_date and type_certification_status.certification_status == certified_status_id:
                    logging.critical(expired_status_id)
                    type_certification_status.certification_status = expired_status_id
                    type_certification_status.assessmentdate = assessment_date
                    type_certification_status.save()

                    centre.requires_manual_certificate_validation = True
                    outdated_centres.append(centre.id)
                    centre.save()

        if outdated_centres:
            subject = "Centres certification expired"
            message = "Following centre has their assessment dates expired today:"
            base_url = "https://"
            base_url += "alpha-" if version(None)["INSTANCE"] == "ALPHA" else "beta-" if version(None)["INSTANCE"] == "BETA" else ""
            base_url += "centres.clarin.eu/admin/centre_registry/centre/{_id}/change/"

            outdated_centres_urls = "\n".join(base_url + _id for _id in outdated_centres)
            message += outdated_centres_urls

            send_mail(subject=subject,
                      message=message,
                      from_email=settings.EMAIL_DEFAULT_FROM,
                      recipient_list=[settings.EMAIL_DEFAULT_TO],
                      fail_silently=False
                      )
