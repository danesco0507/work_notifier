# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0012_auto_20150313_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='notifiedDate',
            field=models.DateField(null=True, verbose_name=b'Fecha de notificacion', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='work',
            name='stateChangedDate',
            field=models.DateField(null=True, verbose_name=b'Fecha cambio estado', blank=True),
            preserve_default=True,
        ),
    ]
