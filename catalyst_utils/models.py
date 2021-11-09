# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from uw_pws import PWS
from uw_gws import GWS
from restclients_core.exceptions import DataFailureException
from logging import getLogger

logger = getLogger(__name__)


class PersonManager(models.Manager):
    pass


class Person(models.Model):
    person_id = models.IntegerField(primary_key=True)
    login_realm_id = models.IntegerField(default=1)
    login_name = models.CharField(max_length=128)
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)
    system_name = models.CharField(max_length=255, null=True)
    system_surname = models.CharField(max_length=255, null=True)
    last_login_date = models.DateTimeField(null=True)

    objects = PersonManager()

    class Meta:
        db_table = 'Person'
        managed = False

    def is_entity(self):
        try:
            entity = PWS().get_entity_by_netid(self.login_name.lower())
            return True
        except DataFailureException as err:
            if err.status == 404:
                return False
            else:
                raise

    def get_uwnetid_admins(self):
        admins = []
        group_id = 'u_netid_{}_admins'.format(self.login_name.lower())
        try:
            for member in GWS().get_members(group_id):
                if member.is_uwnetid():
                    try:
                        person = Person.objects.get(login_name=member.name)
                        admins.append(person)
                    except Person.DoesNotExist:
                        pass
        except DataFailureException as err:
            if err.status == 404:
                pass
            else:
                raise
        return admins

    def csv_data(self):
        return [
            self.login_name,
            self.name,
            self.surname,
            self.last_login_date.isoformat() if (
                self.last_login_date is not None) else None
        ]


class SurveyManager(models.Manager):
    def get_survey_owners(self):
        owners = set()
        for survey in super(SurveyManager, self).all():
            owners.add(survey.person_id)
        return owners


class Survey(models.Model):
    survey_id = models.IntegerField(primary_key=True)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    objects = SurveyManager()

    class Meta:
        db_table = 'Survey'
        managed = False


class GradebookManager(models.Manager):
    pass


class Gradebook(models.Model):
    gradebook_id = models.IntegerField(primary_key=True)
    owner_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)

    objects = GradebookManager()

    class Meta:
        db_table = 'GradeBook'
        managed = False
