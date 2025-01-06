# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase, override_settings
from uw_pws.util import fdao_pws_override
from uw_gws.utilities import fdao_gws_override
from restclients_core.exceptions import DataFailureException, InvalidNetID
from catalyst_utils.dao.person import get_person_data, is_netid


@fdao_pws_override
class PersonDAOFunctionsTest(TestCase):
    @override_settings(CURRENT_USER_GROUP='u_acadev_unittest')
    def test_get_person_data(self):
        self.assertRaises(InvalidNetID, get_person_data, '')
        self.assertRaises(InvalidNetID, get_person_data, '123456')
        self.assertEqual(get_person_data('nobody'), {
            'is_current': False, 'is_person': False})
        self.assertEqual(get_person_data('javerage'), {
            'is_current': True, 'is_person': True, 'preferred_name': 'Jamesy',
            'preferred_surname': 'McJamesy'})

    def test_is_netid(self):
        self.assertEqual(is_netid('javerage'), None)
        self.assertEqual(is_netid('Javerage'), None)
        self.assertEqual(
            is_netid(None),
            'No override user supplied, please enter a UWNetID')
        self.assertEqual(
            is_netid(''), 'No override user supplied, please enter a UWNetID')
        self.assertEqual(is_netid('12345'), 'Not a valid UWNetID: ')
        self.assertEqual(is_netid('doesnotexist'), 'Error (404) : ')
