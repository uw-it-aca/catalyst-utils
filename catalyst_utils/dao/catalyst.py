# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.files.storage import default_storage
from uw_catalyst.gradebook import (
    get_participants_for_gradebook, get_gradebook_export)
from uw_catalyst.survey import (
    get_survey, get_survey_export, get_survey_results,
    get_survey_code_translation)
from restclients_core.exceptions import DataFailureException


def write_file(path, data):
    with default_storage.open(path, mode='wb') as f:
        f.write(data)


def get_survey_attr(survey):
    data = get_survey(survey.survey_id, person=survey.owner)
    return {
        'title': data.get('title'),
        'question_count': data.get('question_count'),
        'response_count': data.get('total_response_count'),
        'last_modified': data.get('modification_date'),
        'last_response': data.get('last_response_date'),
    }


def get_gradebook_attr(gradebook):
    participants = get_participants_for_gradebook(
        gradebook.gradebook_id, person=gradebook.owner)
    return {'participant_count': len(participants)}


def export_survey(survey):
    response = get_survey_export(
        survey.survey_id, person=survey.owner)
    write_file(survey.export_path, response.data)


def export_survey_responses(survey):
    response = get_survey_results(
        survey.survey_id, person=survey.owner)
    write_file(survey.responses_path, response.data)


def export_survey_code_translation(survey):
    response = get_survey_code_translation(
        survey.survey_id, person=survey.owner)
    write_file(survey.code_translation_path, response.data)


def export_gradebook(gradebook):
    response = get_gradebook_export(
        gradebook.gradebook_id, person=gradebook.owner)
    write_file(gradebook.export_path, response.data)
