# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    def add_workgroup(apps, schema_editor):

        Work = apps.get_model("notifier", "Work")
        WorkGroup = apps.get_model("notifier", "WorkGroup")
        for work in Work.objects.all():
            wg = WorkGroup()
            wg.number = work.number
            wg.save()
            work.group = wg
            work.save()

    dependencies = [
        ('notifier', '0010_auto_20150313_1041'),
    ]

    operations = [
        migrations.RunPython(
            add_workgroup
        ),
    ]
