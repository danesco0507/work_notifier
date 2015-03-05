# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0004_work_limitresponsedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='cause',
            name='timeLapseTime',
            field=models.CharField(default=b'Horas', max_length=30, choices=[(b'Dias', b'dias'), (b'Horas', b'horas')]),
            preserve_default=True,
        ),
    ]
