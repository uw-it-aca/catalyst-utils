# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from catalyst_utils.models import Person
from logging import getLogger

logger = getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        Person.objects.update_person_attr()
