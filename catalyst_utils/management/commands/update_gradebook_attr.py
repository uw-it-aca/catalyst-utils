# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from logging import getLogger

from django.core.management.base import BaseCommand

from catalyst_utils.models import Gradebook

logger = getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        Gradebook.objects.update_gradebook_attr()
