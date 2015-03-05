# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0006_auto_20150305_0824'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cause',
            old_name='timeLapse',
            new_name='internTimeLapse',
        ),
        migrations.AddField(
            model_name='cause',
            name='externTimeLapse',
            field=models.IntegerField(default=8, verbose_name=b'time_lapse'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cause',
            name='timeLapseType',
            field=models.CharField(default=b'Horas', max_length=30, choices=[(b'Dias', b'Dias'), (b'Horas', b'Horas')]),
            preserve_default=True,
        ),
    ]
