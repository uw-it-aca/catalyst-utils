# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from catalyst_utils.models import Person, Survey, Gradebook
from uw_pws.util import fdao_pws_override
from uw_gws.utilities import fdao_gws_override


@fdao_pws_override
@fdao_gws_override
class PersonModelTest(TestCase):
    fixtures = ['test_data.json']

    def test_json_data(self):
        person = Person.objects.get(login_name='javerage')
        self.assertEqual(person.json_data(), {
            'login_name': 'javerage', 'name': 'Jamesy McJamesy'})

    def test_csv_data(self):
        person = Person.objects.get(login_name='javerage')
        self.assertEqual(person.csv_data(), [
            'javerage', 'Jamesy', 'McJamesy', '2020/12/01 00:00:00'])

        person = Person.objects.get(login_name='bill')
        self.assertEqual(person.csv_data(), [
            'bill', 'B', 'Avg', None])


class SurveyModelTest(TestCase):
    fixtures = ['test_data.json']

    def test_owner(self):
        survey = Survey.objects.get(survey_id=1)
        self.assertEqual(survey.owner, survey.person)

    def test_json_data(self):
        survey = Survey.objects.get(survey_id=1)
        self.assertEqual(survey.json_data(), {
            'created_date': '2018-01-01T00:00:00+00:00',
            'html_url': 'https://catalyst.uw.edu/webq/survey/javerage/1',
            'name': 'Survey Test',
            'owner': {'login_name': 'javerage', 'name': 'Jamesy McJamesy'}})

        survey = Survey.objects.get(survey_id=2)
        self.assertEqual(survey.json_data(), {
            'created_date': '2017-01-01T00:00:00+00:00',
            'html_url': 'https://catalyst.uw.edu/webq/survey/javerage/2',
            'name': 'Class Survey',
            'owner': {'login_name': 'javerage', 'name': 'Jamesy McJamesy'}})


class GradebookModelTest(TestCase):
    fixtures = ['test_data.json']

    def test_json_data(self):
        gradebook = Gradebook.objects.get(gradebook_id=1)
        self.assertEqual(gradebook.json_data(), {
            'created_date': '2017-01-01T00:00:00+00:00',
            'html_url': 'https://catalyst.uw.edu/gradebook/javerage/1',
            'name': 'CHEM 201 Gradebook',
            'owner': {'login_name': 'javerage', 'name': 'Jamesy McJamesy'}})

        gradebook = Gradebook.objects.get(gradebook_id=2)
        self.assertEqual(gradebook.json_data(), {
            'created_date': '2019-04-01T00:00:00+00:00',
            'html_url': 'https://catalyst.uw.edu/gradebook/javerage/2',
            'name': 'CHEM 202 A Gradebook',
            'owner': {'login_name': 'javerage', 'name': 'Jamesy McJamesy'}})
