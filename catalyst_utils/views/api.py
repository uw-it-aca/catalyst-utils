# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from catalyst_utils.models import Person, Survey, Gradebook
from userservice.user import UserService
from logging import getLogger
import json

logger = getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class APIView(View):
    @property
    def person(self):
        if not hasattr(self, '_person'):
            self._person = Person.objects.get(UserService().get_user())
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
