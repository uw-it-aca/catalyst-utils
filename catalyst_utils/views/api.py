# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from catalyst_utils.models import Person, Survey, Gradebook
from userservice.user import UserService
from logging import getLogger
import json
import re

logger = getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class APIView(View):
    @property
    def person(self):
        if not hasattr(self, '_person'):
            username = UserService().get_user()
            self._person = Person.objects.get(login_name=username)
        return self._person

    @staticmethod
    def json_response(content='', status=200):
        return HttpResponse(json.dumps(content, sort_keys=True),
                            status=status,
                            content_type='application/json')

    @staticmethod
    def error_response(status, message='', content={}):
        content['error'] = str(message)
        return HttpResponse(json.dumps(content),
                            status=status,
                            content_type='application/json')

    @staticmethod
    def file_response(path, filename, content_type='text/csv'):
        if not default_storage.exists(path):
            return self.error_response(404, 'Not Available')

        response = HttpResponse(content='', status=200,
                                content_type=content_type)

        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            re.sub(r'[,/]', '-', filename))

        with default_storage.open(path, mode='r') as f:
            response.content = f.read()
        return response


class SurveyList(APIView):
    def get(self, request, *args, **kwargs):
        try:
            owned_surveys = Survey.objects.by_owner(self.person)
            netid_surveys = Survey.objects.by_netid_admin(self.person)
            admin_surveys = Survey.objects.by_administrator(self.person)
        except Person.DoesNotExist:
            return self.json_response(status=204)

        data = {
            'owned_surveys': [s.json_data() for s in owned_surveys],
            'netid_surveys': [s.json_data() for s in netid_surveys],
            'admin_surveys': [s.json_data() for s in admin_surveys],
        }

        return self.json_response(data)


class GradebookList(APIView):
    def get(self, request, *args, **kwargs):
        try:
            owned_gradebooks = Gradebook.objects.by_owner(self.person)
            netid_gradebooks = Gradebook.objects.by_netid_admin(self.person)
            admin_gradebooks = Gradebook.objects.by_administrator(self.person)
        except Person.DoesNotExist:
            return self.json_response(status=204)

        data = {
            'owned_gradebooks': [s.json_data() for s in owned_gradebooks],
            'netid_gradebooks': [s.json_data() for s in netid_gradebooks],
            'admin_gradebooks': [s.json_data() for s in admin_gradebooks],
        }

        return self.json_response(data)


class SurveyExportFile(APIView):
    def get(self, request, *args, **kwargs):
        try:
            survey = Survey.objects.get(kwargs.get('survey_id'))
            if not survey.is_administrator(self.person):
                return self.error_response(401, 'Not Authorized')
        except Survey.DoesNotExist:
            return self.error_response(404, 'Not Found')

        return self.file_response(survey.export_path, survey.export_filename,
                                  content_type='application/zip')


class SurveyCodeTranslationFile(APIView):
    def get(self, request, *args, **kwargs):
        try:
            survey = Survey.objects.get(kwargs.get('survey_id'))
            if not survey.is_administrator(self.person):
                return self.error_response(401, 'Not Authorized')
            if not survey.is_research_confidential:
                return self.error_response(400, 'Not Available')
        except Survey.DoesNotExist:
            return self.error_response(404, 'Not Found')

        return self.file_response(survey.code_translation_path,
                                  survey.code_translation_filename,
                                  content_type='text/csv')


class SurveyResponsesFile(APIView):
    def get(self, request, *args, **kwargs):
        try:
            survey = Survey.objects.get(kwargs.get('survey_id'))
            if not survey.is_administrator(self.person):
                return self.error_response(401, 'Not Authorized')
        except Survey.DoesNotExist:
            return self.error_response(404, 'Not Found')

        return self.file_response(survey.responses_path,
                                  survey.responses_filename,
                                  content_type='text/csv')


class GradebookExportFile(APIView):
    def get(self, request, *args, **kwargs):
        try:
            gradebook = Gradebook.objects.get(kwargs.get('gradebook_id'))
            if not gradebook.is_administrator(self.person):
                return self.error_response(401, 'Not Authorized')
        except Gradebook.DoesNotExist:
            return self.error_response(404, 'Not Found')

        return self.file_response(gradebook.export_path,
                                  gradebook.export_filename,
                                  content_type='application/vnd.ms-excel')
