# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage
from catalyst_utils.models import Survey
import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
        survey_owners = Survey.objects.get_survey_owners()

        csv.register_dialect('unix_newline', lineterminator='\n')

        survey_owner_outfile = default_storage.open('survey_owners.csv', 'w')
        survey_owner_writer = csv.writer(
            survey_owner_outfile, dialect='unix_newline')
        survey_owner_writer.writerow([
            'uwnetid', 'first_name', 'last_name', 'last_login_date'])

        survey_admin_outfile = default_storage.open(
            'survey_netid_admins.csv', 'w')
        survey_admin_writer = csv.writer(
            survey_admin_outfile, dialect='unix_newline')
        survey_admin_writer.writerow([
            'shared_netid', 'uwnetid', 'first_name', 'last_name',
            'last_login_date'])

        for person in survey_owners:
            if (person.system_name is None and
                    person.system_surname is None and person.is_entity()):
                for admin in person.get_uwnetid_admins():
                    csv_data = [person.login_name] + admin.csv_data()
                    survey_admin_writer.writerow(csv_data)
            else:
                survey_owner_writer.writerow(person.csv_data())

        survey_owner_outfile.close()
        survey_admin_outfile.close()