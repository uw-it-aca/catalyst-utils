# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import re_path
from catalyst_utils.views.pages import HomeView
from catalyst_utils.views.api import SurveyList, GradebookList

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^api/v1/survey$', SurveyList.as_view(), name='survey-list'),
    re_path(r'^api/v1/gradebook$', GradebookList.as_view(),
            name='gradebook-list'),
]
