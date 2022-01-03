# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage
from catalyst_utils.models import Survey, Gradebook
from logging import getLogger
import csv

logger = getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'app', type=str, help='Application (webq|gradebook)')
        parser.add_argument(
            'year', type=int, help='Year (2005-2022) or 0 for all years')

    def handle(self, *args, **options):
        app = options.get('app').lower()
        year = options.get('year')

        csv.register_dialect('unix_newline', lineterminator='\n')
        header = ['uwnetid', 'first_name', 'last_name', 'last_login_date']

        owner_outfile = default_storage.open('{}_owners.csv'.format(app), 'w')
        owner_writer = csv.writer(owner_outfile, dialect='unix_newline')
        owner_writer.writerow(header)

        netid_admin_outfile = default_storage.open(
            '{}_netid_admins.csv'.format(app), 'w')
        netid_admin_writer = csv.writer(netid_admin_outfile,
                                        dialect='unix_newline')
        netid_admin_writer.writerow(header)

        admin_outfile = default_storage.open('{}_admins.csv'.format(app), 'w')
        admin_writer = csv.writer(admin_outfile, dialect='unix_newline')
        admin_writer.writerow(header)

        if 'webq' == app:
            models = Survey.objects.all(year=year)
        else:
            models = Gradebook.objects.all()

        owners = set()
        administrators = set()
        netid_admins = set()
        for model in models:
            owner = model.owner
            if owner:
                if owner.is_person:
                    if owner.is_current:
                        owners.add(owner)
                else:
                    for admin in owner.admins:
                        if admin.is_person and admin.is_current:
                            netid_admins.add(admin)

            for administrator in model.administrators:
                if administrator.is_person:
                    if administrator.is_current:
                        administrators.add(administrator)
                else:
                    for admin in administrator.admins:
                        if admin.is_person and admin.is_current:
                            administrators.add(admin)

        for person in owners:
            owner_writer.writerow(person.csv_data())

        for person in administrators:
            admin_writer.writerow(person.csv_data())

        for person in netid_admins:
            netid_admin_writer.writerow(person.csv_data())

        owner_outfile.close()
        admin_outfile.close()
        netid_admin_outfile.close()
