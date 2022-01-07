# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from uw_pws import PWS
from uw_gws import GWS
from restclients_core.exceptions import DataFailureException, InvalidNetID

pws = PWS()
gws = GWS()


def get_person_data(uwnetid):
    data = {}
    try:
        person = pws.get_person_by_netid(uwnetid.lower())
        data['is_person'] = True
        data['preferred_name'] = person.preferred_first_name
        data['preferred_surname'] = person.preferred_surname
    except DataFailureException as err:
        if err.status == 404:
            data['is_person'] = False
            data['is_current'] = False
        else:
            raise

    if data['is_person']:
        data['is_current'] = gws.is_effective_member(
            settings.CURRENT_USER_GROUP, uwnetid.lower())

    return data


def is_netid(username):
    error_msg = "No override user supplied, please enter a UWNetID"
    if username is not None and len(username) > 0:
        try:
            user = pws.get_entity_by_netid(username.lower())
            if username.lower() == user.uwnetid:
                error_msg = None
            else:
                error_msg = "Current netid: {}, Prior netid: ".format(
                    user.uwnetid)
        except InvalidNetID:
            error_msg = "Not a valid UWNetID: "
        except DataFailureException as err:
            error_msg = "Error ({}) {}: ".format(err.status, err.msg)
    return error_msg
