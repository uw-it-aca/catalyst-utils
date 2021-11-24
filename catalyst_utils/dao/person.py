# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_pws import PWS
from restclients_core.exceptions import DataFailureException
from catalyst_utils.dao.group import is_current_uwnetid

pws = PWS()


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
        data['is_current'] = is_current_uwnetid(uwnetid)

    return data
