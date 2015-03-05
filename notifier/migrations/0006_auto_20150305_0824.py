# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0005_cause_timelapsetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cause',
            old_name='timeLapseTime',
            new_name='timeLapseType',
        ),
    ]
