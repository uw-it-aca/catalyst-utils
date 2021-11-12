# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from uw_pws import PWS
from restclients_core.exceptions import DataFailureException
from catalyst_utils.dao.group import is_current_uwnetid, get_uwnetid_admins
from logging import getLogger

logger = getLogger(__name__)


class PersonManager(models.Manager):
    def update_people(self):
        pass


class Person(models.Model):
    person_id = models.IntegerField(primary_key=True)
    login_realm_id = models.IntegerField(default=1)
    login_name = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)
    last_login_date = models.DateTimeField(null=True)

    objects = PersonManager()

    class Meta:
        db_table = 'Person'
        managed = False

    def _update_attr(self):
        attr, created = PersonAttr.objects.get_or_create(person=self)
        try:
            pws_person = PWS().get_person_by_netid(self.login_name.lower())
            attr.is_person = True
            attr.preferred_name = pws_person.preferred_first_name
            attr.preferred_surname = pws_person.preferred_surname
        except DataFailureException as err:
            if err.status == 404:
                attr.is_person = False
                attr.is_current = False
            else:
                raise

        if attr.is_person:
            attr.is_current = is_current_uwnetid(self.login_name)

        attr.save()
        self.personattr = attr
        if created:
            self.save()

    @property
    def is_person(self):
        try:
            if self.personattr.is_person is None:
                self._update_attr()
        except ObjectDoesNotExist:
            self._update_attr()
        return self.personattr.is_person

    @property
    def is_current(self):
        try:
            if self.personattr.is_current is None:
                self._update_attr()
        except ObjectDoesNotExist:
            self._update_attr()
        return self.personattr.is_current

    @property
    def preferred_name(self):
        try:
            return self.personattr.preferred_name
        except ObjectDoesNotExist:
            self._update_attr()
            return self.personattr.preferred_name

    @property
    def preferred_surname(self):
        try:
            return self.personattr.preferred_surname
        except ObjectDoesNotExist:
            self._update_attr()
            return self.personattr.preferred_surname

    def get_admins(self):
        admins = []
        if not self.is_person:
            for uwnetid in get_uwnetid_admins(self.login_name):
                try:
                    admins.append(Person.objects.get(login_name=uwnetid))
                except Person.DoesNotExist:
                    pass
        return admins

    def csv_data(self):
        if self.preferred_name and self.preferred_surname:
            name = self.preferred_name
            surname = self.preferred_surname
        else:
            name = self.name
            surname = self.surname

        return [
            self.login_name, name, surname,
            self.last_login_date.strftime('%Y/%m/%d %H:%M:%S') if (
                self.last_login_date is not None) else None
        ]


class PersonAttr(models.Model):
    person = models.OneToOneField(Person, primary_key=True,
                                  on_delete=models.CASCADE)
    is_person = models.BooleanField(null=True)
    is_current = models.BooleanField(null=True)
    preferred_name = models.CharField(max_length=255, null=True)
    preferred_surname = models.CharField(max_length=255, null=True)


class SurveyManager(models.Manager):
    def get_survey_owners(self):
        surveys = super(SurveyManager, self).get_queryset().filter(
            creation_date__year=2019)
        owners = set()
        for survey in surveys:
            try:
                owners.add(survey.person)
            except Exception as ex:
                logger.info('person_id {}: {}'.format(survey.person_id, ex))
        return owners


class Survey(models.Model):
    survey_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    creation_date = models.DateTimeField()

    objects = SurveyManager()

    class Meta:
        db_table = 'Survey'
        managed = False


class GradebookManager(models.Manager):
    pass


class Gradebook(models.Model):
    gradebook_id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)

    objects = GradebookManager()

    class Meta:
        db_table = 'GradeBook'
        managed = False
