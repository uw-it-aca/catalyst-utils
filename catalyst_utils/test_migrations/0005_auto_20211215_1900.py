# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


# Generated by Django 2.2.25 on 2021-12-15 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalyst_utils', '0004_auto_20211214_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradebookAttr',
            fields=[
                ('gradebook', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='catalyst_utils.Gradebook')),
                ('participant_count', models.IntegerField(null=True)),
                ('last_updated', models.DateTimeField(null=True)),
                ('update_status', models.IntegerField(default=200)),
                ('last_exported', models.DateTimeField(null=True)),
                ('export_status', models.IntegerField(default=200)),
            ],
        ),
        migrations.RemoveIndex(
            model_name='surveyattr',
            name='update_status_idx',
        ),
        migrations.AddField(
            model_name='surveyattr',
            name='export_status',
            field=models.IntegerField(default=200),
        ),
        migrations.AddField(
            model_name='surveyattr',
            name='last_exported',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='surveyattr',
            name='last_updated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddIndex(
            model_name='surveyattr',
            index=models.Index(fields=['update_status'], name='s_update_status_idx'),
        ),
        migrations.AddIndex(
            model_name='surveyattr',
            index=models.Index(fields=['export_status'], name='s_export_status_idx'),
        ),
        migrations.AddIndex(
            model_name='gradebookattr',
            index=models.Index(fields=['update_status'], name='g_update_status_idx'),
        ),
        migrations.AddIndex(
            model_name='gradebookattr',
            index=models.Index(fields=['export_status'], name='g_export_status_idx'),
        ),
    ]
