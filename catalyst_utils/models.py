# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.conf import settings
from django.utils import timezone
from uw_pws import PWS
from restclients_core.exceptions import DataFailureException
from catalyst_utils.dao.group import is_current_uwnetid, get_group_members
from dateutil.relativedelta import relativedelta
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)


class Person(models.Model):
    """
    Unmanaged read-only Person, data is sourced from solstice.Person table:

    mysqldump -w "login_realm_id = 1" solstice Person > /tmp/person.sql
    """
    person_id = models.IntegerField(primary_key=True)
    login_realm_id = models.IntegerField(default=1)
    login_name = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=255, null=True)
    surname = models.CharField(max_length=255, null=True)
    last_login_date = models.DateTimeField(null=True)

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
        except PersonAttr.DoesNotExist:
            self._update_attr()
        return self.personattr.is_person

    @property
    def is_current(self):
        try:
            if self.personattr.is_current is None:
                self._update_attr()
        except PersonAttr.DoesNotExist:
            self._update_attr()
        return self.personattr.is_current

    @property
    def preferred_name(self):
        try:
            return self.personattr.preferred_name
        except PersonAttr.DoesNotExist:
            self._update_attr()
            return self.personattr.preferred_name

    @property
    def preferred_surname(self):
        try:
            return self.personattr.preferred_surname
        except PersonAttr.DoesNotExist:
            self._update_attr()
            return self.personattr.preferred_surname

    @property
    def admins(self):
        try:
            return self._admins
        except AttributeError:
            self._admins = []
            if not self.is_person:
                group_id = 'u_netid_{}_admins'.format(self.login_name)
                for uwnetid in get_group_members(group_id):
                    try:
                        person = Person.objects.get(login_name=uwnetid)
                        self._admins.append(person)
                    except Person.DoesNotExist:
                        pass
            return self._admins

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


class PeopleInCrowd(models.Model):
    """
    Unmanaged read-only PeopleInCrowd, data is sourced from
    solstice.PeopleInCrowd table
    """
    crowd_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PeopleInCrowd'
        managed = False


class GroupWrapper(models.Model):
    """
    Unmanaged read-only GroupWrapper, data is sourced from
    solstice.GroupWrapper table
    """
    group_id = models.IntegerField(primary_key=True)
    source_key = models.CharField(max_length=255)
    model_package = models.CharField(max_length=255)

    class Meta:
        db_table = 'GroupWrapper'
        managed = False

    @property
    def members(self):
        members = []
        if self.model_package.endswith('Crowd'):
            for pc in PeopleInCrowd.objects.filter(crowd_id=self.source_key):
                try:
                    members.append(pc.person)
                except Person.DoesNotExist:
                    pass
        elif self.model_package.endswith('GWS'):
            for uwnetid in get_group_members(self.source_key, effective=True):
                try:
                    members.append(Person.objects.get(login_name=uwnetid))
                except Person.DoesNotExist:
                    pass
        return members


class RoleImplementationManager(models.Manager):
    def get_administrators(self, object_auth_id):
        authzs = super(RoleImplementationManager, self).get_queryset().filter(
            object_auth_id=object_auth_id,
            role_id=RoleImplementation.ADMINISTRATOR_ROLE_ID)

        people = set()
        for authz in authzs:
            try:
                people.update(authz.group.members)
            except GroupWrapper.DoesNotExist:
                pass
        return people


class RoleImplementation(models.Model):
    """
    Unmanaged read-only RoleImplementation, data is sourced from
    solstice.RoleImplementation table
    """
    ADMINISTRATOR_ROLE_ID = 7

    role_implementation_id = models.IntegerField(primary_key=True)
    role_id = models.IntegerField()
    group = models.ForeignKey(GroupWrapper, on_delete=models.CASCADE)
    object_auth_id = models.IntegerField()

    objects = RoleImplementationManager()

    class Meta:
        db_table = 'RoleImplementation'
        managed = False


class SurveyManager(models.Manager):
    def get_all_surveys(self, year=None):
        if year:
            return super(SurveyManager, self).get_queryset().filter(
                creation_date__year=year).order_by('survey_id')
        else:
            return Survey.objects.all().order_by('survey_id')

    def get_surveys_for_person(self, person):
        pass


class Survey(models.Model):
    """
    Unmanaged read-only Survey, data is sourced from webq.Survey table:

    mysqldump -w "is_quiz = 0 AND is_deleted = 0" webq Survey > /tmp/survey.sql
    """
    survey_id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    creation_date = models.DateTimeField()
    object_auth_id = models.IntegerField()

    objects = SurveyManager()

    class Meta:
        db_table = 'Survey'
        managed = False

    @property
    def owner(self):
        try:
            return self.person
        except Person.DoesNotExist:
            return None

    @property
    def administrators(self):
        return RoleImplementation.objects.get_administrators(
            self.object_auth_id)


class GradebookManager(models.Manager):
    def get_all_gradebooks(self):
        retention = timezone.localtime(timezone.now()) - relativedelta(
            years=settings.GRADEBOOK_RETENTION_YEARS)
        return super(GradebookManager, self).get_queryset().filter(
            create_date__gte=retention).order_by('gradebook_id')

    def get_gradebooks_for_person(self, person):
        pass


class Gradebook(models.Model):
    """
    Unmanaged read-only Gradebook, data is sourced from gradebook.GradeBook:

    mysqldump -w "is_deleted = 0" gradebook GradeBook > /tmp/gradebook.sql
    """
    gradebook_id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=512)
    create_date = models.DateTimeField()
    authz_id = models.IntegerField()

    objects = GradebookManager()

    class Meta:
        db_table = 'GradeBook'
        managed = False

    @property
    def administrators(self):
        return RoleImplementation.objects.get_administrators(self.authz_id)


class PersonAttrManager(models.Manager):
    def update_person_attrs(self):
        pass


class PersonAttr(models.Model):
    """
    Extends solstice.Person data
    """
    person = models.OneToOneField(Person, primary_key=True,
                                  on_delete=models.CASCADE)
    is_person = models.BooleanField(null=True)
    is_current = models.BooleanField(null=True)
    preferred_name = models.CharField(max_length=255, null=True)
    preferred_surname = models.CharField(max_length=255, null=True)
