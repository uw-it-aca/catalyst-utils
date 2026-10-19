# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from logging import getLogger

from django.core.management.base import BaseCommand

from catalyst_utils.models import Survey

logger = getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('uwnetid', help='Survey owner netid')

    def handle(self, *args, **options):
        uwnetid = options.get('uwnetid')
        Survey.objects.export_files_for_owner(uwnetid)
