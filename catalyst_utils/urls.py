# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import re_path
from catalyst_utils.views.pages import HomeView
from catalyst_utils.views.api import (
    SurveyList, GradebookList, SurveyExportFile, SurveyCodeTranslationFile,
    SurveyResponsesFile, GradebookExportFile)

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^api/v1/gradebook$', GradebookList.as_view(),
            name='gradebook-list'),
    re_path(r'^api/v1/gradebook/(?P<gradebook_id>[\d]+)/export$',
            GradebookExportFile.as_view(), name='gradebook-file-export'),
    re_path(r'^api/v1/survey$', SurveyList.as_view(), name='survey-list'),
    re_path(r'^api/v1/survey/(?P<survey_id>[\d]+)/export$',
            SurveyExportFile.as_view(), name='survey-file-export'),
    re_path(r'^api/v1/survey/(?P<survey_id>[\d]+)/code-translation$',
            SurveyCodeTranslationFile.as_view(),
            name='survey-file-codetranslation'),
    re_path(r'^api/v1/survey/(?P<survey_id>[\d]+)/responses$',
            SurveyResponsesFile.as_view(), name='survey-file-responses'),
]
