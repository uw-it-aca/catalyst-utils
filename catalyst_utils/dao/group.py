# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_gws import GWS
from restclients_core.exceptions import DataFailureException


def get_group_members(group_id, effective=False):
    gws = GWS()
    uwnetids = []
    try:
        if effective:
            members = gws.get_effective_members(group_id.lower())
        else:
            members = gws.get_members(group_id.lower())

        for member in members:
            if member.is_uwnetid():
                uwnetids.append(member.name)

    except DataFailureException as err:
        if err.status == 404 or err.status == 401:
            pass
        else:
            raise

    return uwnetids
