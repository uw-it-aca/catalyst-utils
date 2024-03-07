# Copyright 2024 UW-IT, University of Washington
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

        outfile = default_storage.open('{}_users.csv'.format(app), 'w')
        writer = csv.writer(outfile, dialect='unix_newline')
        writer.writerow(header)

        if 'webq' == app:
            models = Survey.objects.all(year=year)
        else:
            models = Gradebook.objects.all()

        users = set()
        for model in models:
            owner = model.owner
            if owner:
                if owner.is_person:
                    if owner.is_current:
                        users.add(owner)
                else:
                    for admin in owner.admins:
                        if admin.is_person and admin.is_current:
                            users.add(admin)

            for administrator in model.administrators:
                if administrator.is_person:
                    if administrator.is_current:
                        users.add(administrator)
                else:
                    for admin in administrator.admins:
                        if admin.is_person and admin.is_current:
                            users.add(admin)

        for person in users:
            writer.writerow(person.csv_data())

        outfile.close()
