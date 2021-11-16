# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from uw_gws import GWS
from restclients_core.exceptions import DataFailureException
from logging import getLogger

logger = getLogger(__name__)
gws = GWS()


def is_current_uwnetid(uwnetid):
    for group_id in getattr(settings, 'CURRENT_USER_GROUPS', []):
        try:
            if gws.is_direct_member(group_id, uwnetid.lower()):
                return True
        except DataFailureException as err:
            logger.info('Group membership check FAILED: {}'.format(err))
    return False


def get_group_members(group_id, effective=False):
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
            logger.info('Group membership FAILED: {}'.format(err))

    return uwnetids
