# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.urls import re_path
from django.views.generic import TemplateView

from catalyst_utils.views.pages import HomeView
from catalyst_utils.views.api import (
    SurveyList, GradebookList, SurveyFile, GradebookFile)

urlpatterns = [
    re_path(r'^api/v1/gradebook$', GradebookList.as_view(),
            name='gradebook-list'),
    re_path(r'^api/v1/gradebook/(?P<gradebook_id>[\d]+)/file$',
            GradebookFile.as_view(), name='gradebook-file'),

    re_path(r'^api/v1/survey$', SurveyList.as_view(), name='survey-list'),
    re_path(r'^api/v1/survey/(?P<survey_id>[\d]+)/file$',
            SurveyFile.as_view(), name='survey-file'),

    re_path(r'^(gradebooks|surveys)$', HomeView.as_view()),
    re_path(r'^$', HomeView.as_view()),
]

# debug routes for developing error pages
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^500$",
            TemplateView.as_view(template_name="500.html"),
            name="500_response",
        ),
        re_path(r"^404$",
            TemplateView.as_view(template_name="404.html"),
            name="404_response",
        )
    ]
