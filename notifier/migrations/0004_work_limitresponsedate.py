# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0003_auto_20150304_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='limitResponseDate',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 5, 14, 19, 0, 217282, tzinfo=utc), verbose_name=b'Fecha limite de respuesta'),
            preserve_default=False,
        ),
    ]
