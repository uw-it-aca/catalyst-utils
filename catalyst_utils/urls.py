# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import re_path

urlpatterns = [
    re_path(r'^api/v1/survey$', SurveyList.as_view(), name='survey-list'),
]
