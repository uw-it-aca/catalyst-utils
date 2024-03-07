# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand, CommandError
from catalyst_utils.models import Survey
from logging import getLogger

logger = getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('uwnetid', help='Survey owner netid')

    def handle(self, *args, **options):
        uwnetid = options.get('uwnetid')
        Survey.objects.export_files_for_owner(uwnetid)
