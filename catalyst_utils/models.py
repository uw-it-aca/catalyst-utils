# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from catalyst_utils.dao.person import get_person_data
from catalyst_utils.dao.group import get_group_members
from catalyst_utils.dao.catalyst import get_survey_attr
from restclients_core.exceptions import DataFailureException
from dateutil.relativedelta import relativedelta
from datetime import datetime
from logging import getLogger
import re

logger = getLogger(__name__)
NETID_ADMIN_GROUP = 'u_netid_{}_admins'


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
    person_id = models.AutoField(primary_key=True)
    login_realm_id = models.IntegerField(blank=True, null=True)
    login_name = models.CharField(max_length=128)
    remote_key = models.CharField(max_length=128, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    system_name = models.CharField(max_length=255, blank=True, null=True)
    system_surname = models.CharField(max_length=255, blank=True, null=True)
    system_email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_sys_modified = models.DateTimeField(blank=True, null=True)
    password_reset_ticket = models.CharField(
        max_length=32, blank=True, null=True)
    last_login_date = models.DateTimeField(blank=True, null=True)

    objects = PersonManager()

    class Meta:
        managed = False
        db_table = 'Person'

    def _update_attr(self):
        data = get_person_data(self.login_name)
        attr, created = PersonAttr.objects.update_or_create(
            person=self, defaults=data)
        if created:
            self.personattr = attr

    @transaction.atomic
    def _update_admins(self):
        if not self.is_person:
            members = []
            group_id = NETID_ADMIN_GROUP.format(self.login_name)
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
            group_id = NETID_ADMIN_GROUP.format(self.login_name)
            for pg in PersonGroup.objects.select_related('person').filter(
                    group_id=group_id):
                admins.append(pg.person)
        return admins

    @property
    def uwnetid(self):
        return self.login_name

    def json_data(self):
        if self.preferred_name and self.preferred_surname:
            name = self.preferred_name
            surname = self.preferred_surname
        else:
            name = self.name
            surname = self.surname

        return {
            'login_name': self.login_name,
            'name': '{} {}'.format(name, surname),
        }

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
        managed = False
        db_table = 'PeopleInCrowd'


class GroupWrapperManager(models.Manager):
    def by_member(self, person):
        source_keys = []
        for key in PeopleInCrowd.objects.filter(person=person).values_list(
                'crowd_id', flat=True):
            source_keys.append(key)

        for key in PersonGroup.objects.filter(person=person).values_list(
                'group_id', flat=True):
            source_keys.append(key)

        return super(GroupWrapperManager, self).get_queryset().filter(
            source_key__in=source_keys)

    def by_netid_admin(self, person):
        owners = []
        pattern = re.compile(NETID_ADMIN_GROUP.format('([a-z0-9]+)'))
        for group_id in PersonGroup.objects.filter(person=person).values_list(
                'group_id', flat=True):
            m = pattern.match(group_id.lower())
            if m:
                try:
                    owners.append(Person.objects.get(login_name=m.group(1)))
                except Person.DoesNotExist:
                    pass
        return owners


class GroupWrapper(models.Model):
    """
    Unmanaged read-only GroupWrapper, data is sourced from
    solstice.GroupWrapper table
    """
    group_id = models.AutoField(primary_key=True)
    source_key = models.CharField(max_length=255)
    authz_id = models.IntegerField(blank=True, null=True)
    model_package = models.CharField(max_length=255)

    objects = GroupWrapperManager()

    class Meta:
        managed = False
        db_table = 'GroupWrapper'
        unique_together = (('model_package', 'source_key'),)

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
                persons.append(member.person)
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

    role_implementation_id = models.AutoField(primary_key=True)
    role_id = models.IntegerField()
    group = models.ForeignKey(GroupWrapper, models.DO_NOTHING)
    object_auth_id = models.IntegerField()

    objects = RoleImplementationManager()

    class Meta:
        managed = False
        db_table = 'RoleImplementation'


class SurveyManager(models.Manager):
    def all(self, year=None):
        if year:
            return super().get_queryset().select_related('person').filter(
                creation_date__year=year).order_by('survey_id')
        else:
            return super().get_queryset().select_related('person').all(
                ).order_by('survey_id')

    def by_owner(self, person):
        return super().get_queryset().filter(person=person)

    def by_netid_admin(self, person):
        owners = GroupWrapper.objects.by_netid_admin(person)
        return super().get_queryset().filter(person__in=owners)

    def by_administrator(self, person):
        auth_ids = RoleImplementation.objects.auth_ids_for_person(person)
        return super().get_queryset().filter(
            object_auth_id__in=auth_ids).exclude(person=person)

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

    def update_survey_attr(self):
        limit = getattr(settings, 'SURVEY_UPDATE_LIMIT', 250)
        for survey in super().get_queryset().select_related('person').all(
                ).order_by('surveyattr__last_updated')[:limit]:
            survey._update_attr()


class Survey(models.Model):
    """
    Unmanaged read-only Survey, data is sourced from webq.Survey table:

    mysqldump -w "is_quiz = 0 AND is_deleted = 0" webq Survey > /tmp/survey.sql
    """
    survey_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, models.DO_NOTHING)
    is_quiz = models.BooleanField(null=True)
    is_deleted = models.BooleanField(null=True)
    title = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    display_screen_title = models.BooleanField(null=True)
    screen_title = models.CharField(max_length=255, blank=True, null=True)
    display_screen_subtitle = models.BooleanField(null=True)
    screen_subtitle = models.CharField(max_length=255, blank=True, null=True)
    display_screen_name = models.BooleanField(null=True)
    screen_name = models.CharField(max_length=255, blank=True, null=True)
    display_screen_email = models.BooleanField(null=True)
    screen_email = models.CharField(max_length=255, blank=True, null=True)
    display_confirmation_code = models.BooleanField(null=True)
    display_closing_content = models.BooleanField(null=True)
    closing_content = models.TextField(blank=True, null=True)
    auto_number = models.BooleanField(null=True)
    auto_number_type_id = models.IntegerField(blank=True, null=True)
    auto_number_format_id = models.IntegerField(blank=True, null=True)
    auto_number_prefix = models.CharField(
        max_length=255, blank=True, null=True)
    send_notification = models.BooleanField(null=True)
    announcement_subject = models.TextField(blank=True, null=True)
    announcement_body = models.TextField(blank=True, null=True)
    announcement_sent = models.DateTimeField(blank=True, null=True)
    reminder_subject = models.TextField(blank=True, null=True)
    reminder_body = models.TextField(blank=True, null=True)
    reminder_sent = models.DateTimeField(blank=True, null=True)
    send_announcement = models.BooleanField(null=True)
    send_reminder = models.BooleanField(null=True)
    reminder_date = models.DateTimeField(blank=True, null=True)
    announcement_date = models.DateTimeField(blank=True, null=True)
    has_time_limit = models.BooleanField(null=True)
    time_limit_hour = models.CharField(max_length=5, blank=True, null=True)
    time_limit_min = models.CharField(max_length=5, blank=True, null=True)
    time_limit = models.IntegerField(blank=True, null=True)
    reminder_frequency_id = models.IntegerField(blank=True, null=True)
    tags_match_email = models.BooleanField(null=True)
    requires_notification = models.DateTimeField(blank=True, null=True)
    account_copy_sender = models.IntegerField(blank=True, null=True)
    account_copy_reciever = models.IntegerField(blank=True, null=True)
    account_copy_date = models.DateTimeField(blank=True, null=True)
    origin_survey_id = models.IntegerField(blank=True, null=True)
    rejected_survey_copy = models.BooleanField(null=True)
    copied_questions = models.BooleanField(null=True)
    copied_security = models.BooleanField(null=True)
    copied_announcements = models.BooleanField(null=True)
    copied_reminders = models.BooleanField(null=True)
    copied_participant_experience = models.BooleanField(null=True)
    copied_appearance = models.BooleanField(null=True)
    copied_custom_name = models.BooleanField(null=True)
    copied_notification = models.BooleanField(null=True)
    notification_copied_settings = models.BooleanField(null=True)
    object_auth_id = models.IntegerField(blank=True, null=True)
    allows_backtracking = models.BooleanField(null=True)
    allows_saveforlater = models.BooleanField(null=True)
    allows_confirm_responses = models.BooleanField(null=True)
    allows_modifying_finished = models.BooleanField(null=True)
    allows_multiple_submissions = models.BooleanField(null=True)
    display_results_summary = models.BooleanField(null=True)
    display_results_summary_questions = models.BooleanField(null=True)
    display_results_summary_score = models.BooleanField(null=True)
    display_results_summary_feedback = models.BooleanField(null=True)
    display_results_summary_correct_answer = models.BooleanField(null=True)
    display_results_summary_total_score = models.BooleanField(null=True)
    display_results_summary_stats = models.BooleanField(null=True)
    display_results_summary_while_published = models.BooleanField(null=True)
    display_results_summary_custom_interval = models.BooleanField(null=True)
    display_results_summary_interval_length = models.BooleanField(null=True)
    display_results_summary_interval_scale = models.CharField(
        max_length=3, blank=True, null=True)
    is_research_confidential = models.BooleanField(null=True)
    is_research_anonymous = models.BooleanField(null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    unpublish_date = models.DateTimeField(blank=True, null=True)
    security_type = models.CharField(max_length=13, blank=True, null=True)
    in_conversion = models.BooleanField(null=True)
    copied_skip_logic = models.BooleanField(null=True)

    objects = SurveyManager()

    class Meta:
        managed = False
        db_table = 'Survey'

    @property
    def owner(self):
        return self.person

    @property
    def administrators(self):
        return RoleImplementation.objects.administrators(self.object_auth_id)

    @property
    def name(self):
        # Return the title from SurveyAttr, not Survey
        try:
            return self.surveyattr.title
        except SurveyAttr.DoesNotExist:
            self._update_attr()
            return self.surveyattr.title

    @property
    def question_count(self):
        try:
            return self.surveyattr.question_count
        except SurveyAttr.DoesNotExist:
            self._update_attr()
            return self.surveyattr.question_count

    @property
    def response_count(self):
        try:
            return self.surveyattr.response_count
        except SurveyAttr.DoesNotExist:
            self._update_attr()
            return self.surveyattr.response_count

    @property
    def export_path(self):
        return '/survey/{}/{}/export.zip'.format(
            self.person.login_name, self.survey_id)

    @property
    def responses_path(self):
        return '/survey/{}/{}/responses.csv'.format(
            self.person.login_name, self.survey_id)

    @property
    def code_translation_path(self):
        return '/survey/{}/{}/code_translation.csv'.format(
            self.person.login_name, self.survey_id)

    def json_data(self):
        return {
            'name': self.name,
            'created_date': self.creation_date.isoformat(),
            'html_url': 'https://catalyst.uw.edu/webq/survey/{}/{}'.format(
                self.person.login_name, self.survey_id),
            'owner': self.person.json_data(),
            'question_count': self.question_count,
            'response_count': self.response_count,
            'is_research_confidential': self.is_research_confidential,
            'is_research_anonymous': self.is_research_anonymous,
        }

    def _update_attr(self):
        try:
            data = get_survey_attr(self)
            attr, created = SurveyAttr.objects.update_or_create(
                survey=self, defaults=data)
            if created:
                self.surveyattr = attr
        except DataFailureException as ex:
            logger.info('Survey update failed: {}'.format(ex))


class GradebookManager(models.Manager):
    def all(self):
        retention = timezone.localtime(timezone.now()) - relativedelta(
            years=settings.GRADEBOOK_RETENTION_YEARS)
        return super().get_queryset().select_related('owner').filter(
            create_date__gte=retention).order_by('gradebook_id')

    def by_owner(self, person):
        return super().get_queryset().filter(owner=person)

    def by_netid_admin(self, person):
        owners = GroupWrapper.objects.by_netid_admin(person)
        return super().get_queryset().filter(owner__in=owners)

    def by_administrator(self, person):
        auth_ids = RoleImplementation.objects.auth_ids_for_person(person)
        return super().get_queryset().filter(
            authz_id__in=auth_ids).exclude(owner=person)

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
    gradebook_id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    authz_id = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(blank=True, null=True)
    last_init_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(null=True)
    calculate_total_scores = models.BooleanField(null=True)
    calculate_class_grades = models.BooleanField(null=True)
    total_score_id = models.IntegerField(blank=True, null=True)
    class_grade_id = models.IntegerField(blank=True, null=True)
    count_blanks = models.BooleanField(null=True)
    lowest_conversion_range_grade = models.TextField(blank=True, null=True)
    include_dropped_in_stats = models.BooleanField(null=True)

    objects = GradebookManager()

    class Meta:
        managed = False
        db_table = 'GradeBook'

    @property
    def administrators(self):
        return RoleImplementation.objects.administrators(self.authz_id)

    @property
    def export_path(self):
        return '/gradebook/{}/{}/export.xls'.format(
            self.owner.login_name, self.gradebook_id)

    def json_data(self):
        return {
            'name': self.name,
            'created_date': self.create_date.isoformat(),
            'html_url': 'https://catalyst.uw.edu/gradebook/{}/{}'.format(
                self.owner.login_name, self.gradebook_id),
            'owner': self.owner.json_data(),
        }


class SurveyAttr(models.Model):
    """
    Extends webq.Survey data
    """
    survey = models.OneToOneField(Survey, models.DO_NOTHING, primary_key=True)
    question_count = models.IntegerField(null=True)
    response_count = models.IntegerField(null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)


class PersonAttr(models.Model):
    """
    Extends solstice.Person data
    """
    person = models.OneToOneField(Person, models.DO_NOTHING, primary_key=True)
    is_person = models.BooleanField(null=True)
    is_current = models.BooleanField(null=True)
    preferred_name = models.CharField(max_length=255, blank=True, null=True)
    preferred_surname = models.CharField(max_length=255, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)


class PersonGroup(models.Model):
    group_id = models.CharField(max_length=255)
    person = models.ForeignKey(Person, models.DO_NOTHING)

    class Meta:
        indexes = [
            models.Index(fields=['group_id'], name='group_id_idx'),
        ]
