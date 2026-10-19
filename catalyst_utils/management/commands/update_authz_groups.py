# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from logging import getLogger

from django.core.management.base import BaseCommand

from catalyst_utils.models import Gradebook, Survey

logger = getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        Survey.objects.update_authz_groups()
        Gradebook.objects.update_authz_groups()
