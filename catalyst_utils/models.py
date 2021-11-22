# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from uw_pws import PWS
from restclients_core.exceptions import DataFailureException
from catalyst_utils.dao.group import is_current_uwnetid, get_group_members
from dateutil.relativedelta import relativedelta
from datetime import datetime
from logging import getLogger
import re

logger = getLogger(__name__)


class PersonManager(models.Manager):
    def update_netid_admins(self):
        for person in super().get_queryset().filter(
                personattr__is_person=False):
            person._update_admins()

    def update_person_attr(self):
        limit = getattr(settings, 'PERSON_UPDATE_LIMIT', 250)
        for person in super().get_queryset().filter(
                    personattr__is_person=True, personattr__is_current=True
                ).order_by('personattr__last_updated')[:limit]:
            person._update_attr()


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

    @transaction.atomic
    def _update_admins(self):
        if not self.is_person:
            members = []
            group_id = 'u_netid_{}_admins'.format(self.login_name)
            for uwnetid in get_group_members(group_id):
                try:
                    person = Person.objects.get(login_name=uwnetid)
                    pg, _ = PersonGroup.objects.get_or_create(
                        group_id=group_id, person=person)
                    members.append(person)
                except Person.DoesNotExist:
                    pass

            PersonGroup.objects.filter(group_id=group_id).exclude(
                person__in=members).delete()

    @property
    def is_person(self):
        try:
            return self.personattr.is_person
        except PersonAttr.DoesNotExist:
            self._update_attr()
            return self.personattr.is_person

    @property
    def is_current(self):
        try:
            return self.personattr.is_current
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
        admins = []
        if not self.is_person:
            group_id = 'u_netid_{}_admins'.format(self.login_name)
            for pg in PersonGroup.objects.select_related('person').filter(
                    group_id=group_id):
                admin.append(pg.person)
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


class GroupWrapperManager(models.Manager):
    def by_member(self, person):
        source_keys = PeopleInCrowd.objects.filter(person=person).values_list(
            'crowd_id', flat=True)
        source_keys += PersonGroup.objects.filter(person=person).values_list(
            'group_id', flat=True)

        return super(GroupWrapperManager, self).get_queryset().filter(
            source_key__in=source_keys)


class GroupWrapper(models.Model):
    """
    Unmanaged read-only GroupWrapper, data is sourced from
    solstice.GroupWrapper table
    """
    group_id = models.IntegerField(primary_key=True)
    source_key = models.CharField(max_length=255)
    model_package = models.CharField(max_length=255)

    objects = GroupWrapperManager()

    class Meta:
        db_table = 'GroupWrapper'
        managed = False

    @property
    def members(self):
        if self.model_package.endswith('Crowd'):
            members = PeopleInCrowd.objects.select_related('person').filter(
                crowd_id=self.source_key)
        else:
            members = PersonGroup.objects.select_related('person').filter(
                group_id=self.source_key)

        persons = []
        for member in members:
            try:
                people.append(member.person)
            except Person.DoesNotExist:
                pass
        return persons

    @transaction.atomic
    def update_membership(self):
        if not self.model_package.endswith('GWS'):
            raise NotImplementedError(self.model_package)

        members = []
        for uwnetid in get_group_members(self.source_key, effective=True):
            try:
                person = Person.objects.get(login_name=uwnetid)
                pg, _ = PersonGroup.objects.get_or_create(
                    group_id=self.source_key, person=person)
                members.append(person)
            except Person.DoesNotExist:
                pass

        PersonGroup.objects.filter(group_id=self.source_key).exclude(
            person__in=members).delete()


class RoleImplementationManager(models.Manager):
    def authorizations(self, object_auth_id):
        return super().get_queryset().select_related('group').filter(
            object_auth_id=object_auth_id,
            role_id=RoleImplementation.ADMINISTRATOR_ROLE_ID)

    def auth_ids_for_person(self, person):
        return super().get_queryset().filter(
                group__in=GroupWrapper.objects.by_member(person),
                role_id=RoleImplementation.ADMINISTRATOR_ROLE_ID
            ).values_list('object_auth_id', flat=True)

    def administrators(self, object_auth_id):
        people = set()
        for authz in self.authorizations(object_auth_id):
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
    def all(self, year=None):
        if year:
            return super().get_queryset().select_related('person').filter(
                creation_date__year=year).order_by('survey_id')
        else:
            return super().get_queryset().select_related('person').all(
                ).order_by('survey_id')

    def by_owner(self, person):
        return super().get_queryset().filter(person=person).order_by(
            'survey_id')

    def by_netid_admin(self, person):
        owners = []
        for group_id in PersonGroup.objects.filter(person=person).values_list(
                'group_id', flat=True):
            m = re.match(r'^u_netid_([a-z0-9+])_admins$', re.I)
            netid = m.group(0)

    def by_administrator(self, person):
        auth_ids = RoleImplementation.objects.auth_ids_for_person(person)
        return super().get_queryset().filter(object_auth_id__in=auth_ids)

    def update_authz_groups(self):
        groups = set()
        for object_auth_id in super().get_queryset().all().values_list(
                'object_auth_id', flat=True):
            for authz in RoleImplementation.objects.authorizations(
                    object_auth_id):
                try:
                    if authz.group not in groups:
                        authz.group.update_membership()
                        groups.add(authz.group)
                except (NotImplementedError, GroupWrapper.DoesNotExist):
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
        return RoleImplementation.objects.administrators(self.object_auth_id)


class GradebookManager(models.Manager):
    def all(self):
        retention = timezone.localtime(timezone.now()) - relativedelta(
            years=settings.GRADEBOOK_RETENTION_YEARS)
        return super().get_queryset().select_related('owner').filter(
            create_date__gte=retention).order_by('gradebook_id')

    def by_owner(self, person):
        pass

    def by_administrator(self, person):
        pass

    def update_authz_groups(self):
        groups = set()
        for authz_id in super().get_queryset().all().values_list(
                'authz_id', flat=True):
            for authz in RoleImplementation.objects.authorizations(authz_id):
                try:
                    if authz.group not in groups:
                        authz.group.update_membership()
                        groups.add(authz.group)
                except (NotImplementedError, GroupWrapper.DoesNotExist):
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
        return RoleImplementation.objects.administrators(self.authz_id)


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
    last_updated = models.DateTimeField(auto_now=True)


class PersonGroup(models.Model):
    group_id = models.CharField(max_length=255)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['group_id'], name='group_id_idx'),
        ]
