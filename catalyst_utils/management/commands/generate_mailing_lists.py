# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage
from catalyst_utils.models import Survey
import csv


class Command(BaseCommand):
    def handle(self, *args, **options):
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
            'uwnetid', 'first_name', 'last_name', 'last_login_date',
            'shared_netids'])

        admins = {}
        for person in Survey.objects.get_survey_owners():
            if person.is_person:
                if person.is_current:
                    survey_owner_writer.writerow(person.csv_data())
            else:
                for admin in person.get_admins():
                    if admin.is_person and admin.is_current:
                        if admin.person_id in admins:
                            admins[admin.person_id].get(
                                'shared_netids', []).append(person.login_name)
                        else:
                            admins[admin.person_id] = {
                                'person': admin,
                                'shared_netids': [person.login_name],
                            }

        for person_id in admins:
            csv_data = admins[person_id]['person'].csv_data()
            csv_data.append(','.join(admins[person_id]['shared_netids']))
            survey_admin_writer.writerow(csv_data)

        survey_owner_outfile.close()
        survey_admin_outfile.close()
