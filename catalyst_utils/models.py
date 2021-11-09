# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from logging import getLogger

logger = getLogger(__name__)


class ObjectAuth(models.Model):
    object_auth_id = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=32)
    group = models.CharField(max_length=100)


class PersonManager(models.Manager):
    pass


class Person(models.Model):
    person_id = models.IntegerField(primary_key=True)
    netid = models.CharField(max_length=32)
    is_entity = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    last_login = models.DateTimeField(null=True)

    objects = PersonManager()


class SurveyManager(models.Manager):
    pass


class Survey(models.Model):
    survey_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField()
    is_research_confidential = models.BooleanField(default=False)
    is_research_anonymous = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True)
    unpublish_date = models.DateTimeField(null=True)
    security_type = models.SlugField(null=True)
    object_auth = models.ForeignKey(ObjectAuth, on_delete=models.CASCADE)

    objects = SurveyManager()


class GradebookManager(models.Manager):
    pass


class Gradebook(models.Model):
    gradebook_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField()
    object_auth = models.ForeignKey(ObjectAuth, on_delete=models.CASCADE)

    objects = GradebookManager()
