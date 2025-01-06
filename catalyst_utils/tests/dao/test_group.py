# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from uw_gws.utilities import fdao_gws_override
from uw_gws.exceptions import InvalidGroupID
from catalyst_utils.dao.group import get_group_members


@fdao_gws_override
class GroupDAOFunctionsTest(TestCase):
    def test_get_group_members(self):
        group_id = 'u_acadev_unittest'
        self.assertEqual(len(get_group_members(group_id)), 2)
        self.assertEqual(len(get_group_members(group_id, effective=True)), 3)
        self.assertEqual(len(get_group_members('u_acadev_doesnotexist')), 0)
        self.assertRaises(InvalidGroupID, get_group_members, '')
