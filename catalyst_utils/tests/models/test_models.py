# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from catalyst_utils.models import Person, Survey, Gradebook
from uw_pws.util import fdao_pws_override


@fdao_pws_override
class PersonModelTest(TestCase):
    def setUp(self):
        person, _ = Person.objects.get_or_create(login_name='javerage')
        self.person = person

    def test_json_data(self):
        self.assertEqual(self.person.json_data(), {
            'login_name': 'javerage', 'name': 'Jamesy McJamesy'})

    def test_csv_data(self):
        self.assertEqual(self.person.csv_data(), [
            'javerage', 'Jamesy', 'McJamesy', None])


class SurveyModelTest(TestCase):
    pass


class GradebookModelTest(TestCase):
    pass
