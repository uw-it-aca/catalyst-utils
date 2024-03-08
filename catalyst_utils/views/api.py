# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from catalyst_utils.models import Person, Survey, Gradebook
from catalyst_utils.dao.file import read_file, build_archive
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
    def file_response(content, filename, content_type='text/csv'):
        response = HttpResponse(content=content, status=200,
                                content_type=content_type)

        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            re.sub(r'[,/]', '-', filename))

        return response

    @staticmethod
    def sorted_tools(tools):
        return sorted(tools,
                      key=lambda t: (t['created_date'], t['name'].upper()),
                      reverse=True)


class SurveyList(APIView):
    def get(self, request, *args, **kwargs):
        try:
            owned_surveys = Survey.objects.by_owner(self.person)
            netid_surveys = Survey.objects.by_netid_admin(self.person)
            admin_surveys = Survey.objects.by_administrator(self.person)
        except Person.DoesNotExist:
            return self.json_response(status=204)

        data = {
            'owned_surveys': self.sorted_tools(
                [s.json_data() for s in owned_surveys]),
            'netid_surveys': self.sorted_tools(
                [s.json_data() for s in netid_surveys]),
            'admin_surveys': self.sorted_tools(
                [s.json_data() for s in admin_surveys]),
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
            'owned_gradebooks': self.sorted_tools(
                [s.json_data() for s in owned_gradebooks]),
            'netid_gradebooks': self.sorted_tools(
                [s.json_data() for s in netid_gradebooks]),
            'admin_gradebooks': self.sorted_tools(
                [s.json_data() for s in admin_gradebooks]),
        }

        return self.json_response(data)


class SurveyFile(APIView):
    def get(self, request, *args, **kwargs):
        survey_id = kwargs.get('survey_id')
        try:
            survey = Survey.objects.get(survey_id=survey_id)
        except Survey.DoesNotExist:
            return self.error_response(404, 'Not Found')

        if not survey.is_administrator(self.person):
            return self.error_response(401, 'Not Authorized')

        try:
            archive = build_archive([survey.export_path,
                                     survey.responses_path,
                                     survey.code_translation_path])
        except ObjectDoesNotExist:
            return self.error_response(404, 'Not Available')

        return self.file_response(archive, survey.filename,
                                  content_type='application/zip')


class GradebookFile(APIView):
    def get(self, request, *args, **kwargs):
        gradebook_id = kwargs.get('gradebook_id')
        try:
            gradebook = Gradebook.objects.get(gradebook_id=gradebook_id)
        except Gradebook.DoesNotExist:
            return self.error_response(404, 'Not Found')

        if not gradebook.is_administrator(self.person):
            return self.error_response(401, 'Not Authorized')

        try:
            return self.file_response(read_file(gradebook.export_path),
                                      gradebook.filename,
                                      content_type='application/vnd.ms-excel')
        except ObjectDoesNotExist:
            return self.error_response(404, 'Not Available')
