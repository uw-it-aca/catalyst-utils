# Copyright 2026 UW-IT, University of Washington
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
    if username is None or not len(username):
        return "No override user supplied, please enter a UWNetID"
    if not pws.valid_uwnetid(username.lower()):
        return "Not a valid UWNetID: "
    return
