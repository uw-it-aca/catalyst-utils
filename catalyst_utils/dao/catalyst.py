# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_catalyst.gradebook import get_gradebook_export
from restclients_core.exceptions import DataFailureException


def export_gradebook(gradebook_id, person):
    return get_gradebook_export(gradebook_id, person=person)
