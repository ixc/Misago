# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from extras.oms_json.fields import JSONField

from misago.acl.models import permissions_default


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('name', models.CharField(max_length=255)),
                ('special_role', models.CharField(max_length=255, null=True, blank=True)),
                ('permissions', JSONField(default=permissions_default)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, ),
        ),
    ]
