# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# Generated by Django 2.2.25 on 2021-12-14 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalyst_utils', '0003_auto_20211210_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyattr',
            name='update_status',
            field=models.IntegerField(default=200),
        ),
        migrations.AddIndex(
            model_name='surveyattr',
            index=models.Index(fields=['update_status'], name='update_status_idx'),
        ),
    ]