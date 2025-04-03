from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.utils import timezone
from django.test.client import RequestFactory
from django.utils.timezone import localdate

import logging

from centre_registry.models import Centre, CertificationStatus


class Command(BaseCommand):
    help = 'Command to update certification status based on expiration date'

    def handle(self, *args, **options):
        today_date = timezone.now()
        print("TODAY DATE")
        print(today_date)

        centres = Centre.objects.all()
        expired_status_id = CertificationStatus.objects.get(status="Pending (recertification)")
        outdated_centres = []

        for centre in centres:
            centre_types = centre.type.all()
            assessment_dates = centre.assessmentdates.all()
            print(assessment_dates)
            logging.critical(assessment_dates)
            logging.critical("HERE")
            for assessment_date in assessment_dates:
                logging.critical("HERE1")
                print(assessment_date)
                assessment_date_type = assessment_date.type
                if assessment_date_type in centre_types:
                    due_date = assessment_date.duedate
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    print(due_date)
                    print(today_date)
                    print(due_date > today_date)
                    logging.critical("DUE")
                    logging.critical(due_date)
                    logging.critical("TODAY")
                    logging.critical(today_date)
                    logging.critical(due_date > today_date)
                    if due_date > today_date:
                        if not centre.requires_manual_certificate_validation:
                            centre.type_certification_status = expired_status_id
                            centre.requires_manual_certificate_validation = True
                            outdated_centres.append(centre.name)
                            centre.save()

        if outdated_centres:
            outdated_centres = '\n'.join(outdated_centres)
            subject = "Centres certification expired"
            message = "Following centre has their assessment dates expired today:" + outdated_centres

            print(message)
            send_mail(subject=subject,
                      message=message,
                      from_email='centre-registry@clarin.eu',
                      recipient_list=['michal@clarin.eu'],
                      fail_silently=False
                      )
