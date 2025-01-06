# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from django.utils import timezone
from catalyst_utils.models import Person, Survey, Gradebook
from uw_pws.util import fdao_pws_override
from uw_gws.utilities import fdao_gws_override
from datetime import datetime
import mock


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

    def test_file_paths(self):
        survey = Survey.objects.get(survey_id=1)
        self.assertEqual(survey.export_path,
                         '/survey/javerage/1/export.zip')
        self.assertEqual(survey.responses_path,
                         '/survey/javerage/1/responses.csv')
        self.assertEqual(survey.code_translation_path,
                         '/survey/javerage/1/code_translation.csv')

    def test_filename(self):
        survey = Survey.objects.get(survey_id=1)
        self.assertEqual(survey.filename, 'javerage-Survey Test.zip')

    def test_json_data(self):
        survey = Survey.objects.get(survey_id=1)
        self.assertEqual(survey.json_data(), {
            'id': 1,
            'created_date': '2018-01-01T00:00:00+00:00',
            'html_url': 'https://catalyst.uw.edu/webq/survey/javerage/1',
            'name': 'Survey Test',
            'question_count': 5,
            'response_count': 2,
            'is_research_confidential': True,
            'is_research_anonymous': False,
            'download_url': '/api/v1/survey/1/file',
            'owner': {'login_name': 'javerage', 'name': 'Jamesy McJamesy'}})

        survey = Survey.objects.get(survey_id=2)
        self.assertEqual(survey.json_data(), {
            'id': 2,
            'created_date': '2017-01-01T00:00:00+00:00',
            'html_url': 'https://catalyst.uw.edu/webq/survey/javerage/2',
            'name': 'Class Survey',
            'question_count': 15,
            'response_count': 220,
            'is_research_confidential': False,
            'is_research_anonymous': False,
            'download_url': '/api/v1/survey/2/file',
            'owner': {'login_name': 'javerage', 'name': 'Jamesy McJamesy'}})


class GradebookModelTest(TestCase):
    fixtures = ['test_data.json']

    @mock.patch.object(timezone, 'now')
    def test_retention_date(self, mock_now):
        mock_now.return_value = timezone.make_aware(datetime(2013, 7, 1))
        self.assertEqual(Gradebook.retention_date().isoformat(),
                         '2008-07-01T00:00:00-07:00')

        mock_now.return_value = timezone.make_aware(datetime(2013, 12, 31))
        self.assertEqual(Gradebook.retention_date().isoformat(),
                         '2008-07-01T00:00:00-07:00')

        mock_now.return_value = timezone.make_aware(datetime(2014, 1, 1))
        self.assertEqual(Gradebook.retention_date().isoformat(),
                         '2008-07-01T00:00:00-07:00')

        mock_now.return_value = timezone.make_aware(datetime(2014, 6, 30))
        self.assertEqual(Gradebook.retention_date().isoformat(),
                         '2008-07-01T00:00:00-07:00')

    def test_export_path(self):
        gradebook = Gradebook.objects.get(gradebook_id=1)
        self.assertEqual(gradebook.export_path,
                         '/gradebook/javerage/1/export.xls')

        gradebook = Gradebook.objects.get(gradebook_id=2)
        self.assertEqual(gradebook.export_path,
                         '/gradebook/javerage/2/export.xls')

    def test_filename(self):
        gradebook = Gradebook.objects.get(gradebook_id=1)
        self.assertEqual(gradebook.filename,
                         'javerage-CHEM 201 Gradebook.xls')

        gradebook = Gradebook.objects.get(gradebook_id=2)
        self.assertEqual(gradebook.filename,
                         'javerage-CHEM 202 A Gradebook.xls')

    def test_json_data(self):
        gradebook = Gradebook.objects.get(gradebook_id=1)
        self.assertEqual(gradebook.json_data(), {
            'created_date': '2022-01-01T00:00:00+00:00',
            'html_url': 'https://catalyst.uw.edu/gradebook/javerage/1',
            'name': 'CHEM 201 Gradebook',
            'participant_count': 25,
            'download_url': '/api/v1/gradebook/1/file',
            'owner': {'login_name': 'javerage', 'name': 'Jamesy McJamesy'}})

        gradebook = Gradebook.objects.get(gradebook_id=2)
        self.assertEqual(gradebook.json_data(), {
            'created_date': '2022-04-01T00:00:00+00:00',
            'html_url': 'https://catalyst.uw.edu/gradebook/javerage/2',
            'name': 'CHEM 202 A Gradebook',
            'participant_count': 40,
            'download_url': '/api/v1/gradebook/2/file',
            'owner': {'login_name': 'javerage', 'name': 'Jamesy McJamesy'}})
