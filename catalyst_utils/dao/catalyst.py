# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.files.storage import default_storage
from uw_catalyst.gradebook import get_gradebook_export
from uw_catalyst.survey import (
    get_survey, get_survey_export, get_survey_results,
    get_survey_code_translation)
from restclients_core.exceptions import DataFailureException


def get_survey(survey):
    data = get_survey(survey.survey_id, person=survey.owner)
    return {
        'question_count': data.get('question_count'),
        'response_count': data.get('total_response_count'),
    }


def export_survey(survey):
    pass


def export_survey_responses(survey):
    pass


def export_survey_code_translation(survey):
    pass


def export_gradebook(gradebook):
    response = get_gradebook_export(
        gradebook.gradebook_id, person=gradebook.owner)

    with default_storage.open(gradebook.export_path, mode='wb') as f:
        f.write(response.data)
