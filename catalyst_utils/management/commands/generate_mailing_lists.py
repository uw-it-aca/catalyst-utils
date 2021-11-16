# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage
from catalyst_utils.models import Survey
from logging import getLogger
import csv

logger = getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        csv.register_dialect('unix_newline', lineterminator='\n')
        header = ['uwnetid', 'first_name', 'last_name', 'last_login_date']

        survey_owner_outfile = default_storage.open('survey_owners.csv', 'w')
        survey_owner_writer = csv.writer(
            survey_owner_outfile, dialect='unix_newline')
        survey_owner_writer.writerow(header)

        survey_netid_admin_outfile = default_storage.open(
            'survey_netid_admins.csv', 'w')
        survey_netid_admin_writer = csv.writer(
            survey_netid_admin_outfile, dialect='unix_newline')
        survey_netid_admin_writer.writerow(header + ['shared_netids'])

        survey_admin_outfile = default_storage.open('survey_admins.csv', 'w')
        survey_admin_writer = csv.writer(
            survey_admin_outfile, dialect='unix_newline')
        survey_admin_writer.writerow(header)

        owners = set()
        administrators = set()
        netid_admins = {}
        for survey in Survey.objects.get_all_surveys(year=None):
            owner = survey.owner
            if owner.is_person:
                if owner.is_current:
                    owners.add(owner)
            else:
                for admin in owner.admins:
                    if admin.is_person and admin.is_current:
                        if admin.person_id in netid_admins:
                            netid_admins[admin.person_id].get(
                                'shared_netids', []).append(owner.login_name)
                        else:
                            netid_admins[admin.person_id] = {
                                'person': admin,
                                'shared_netids': [owner.login_name],
                            }

            for administrator in survey.administrators:
                if administrator.is_person:
                    if administrator.is_current:
                        administrators.add(administrator)
                else:
                    logger.info('Non-personal administrator: {}'.format(
                        administrator.login_name))

        for person in owners:
            survey_owner_writer.writerow(person.csv_data())

        for person in administrators:
            survey_admin_writer.writerow(person.csv_data())

        for person_id in netid_admins:
            person = netid_admins[person_id]['person']
            csv_data = person.csv_data()
            csv_data.append('|'.join(netid_admins[person_id]['shared_netids']))
            survey_netid_admin_writer.writerow(csv_data)

        survey_owner_outfile.close()
        survey_admin_outfile.close()
        survey_netid_admin_outfile.close()
