# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifier', '0002_auto_20150226_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='createdDate',
            field=models.DateField(default=datetime.datetime(2015, 3, 4, 14, 14, 54, 392173, tzinfo=utc), verbose_name=b'Fecha de Creacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='work',
            name='state',
            field=models.CharField(default=b'No Notificado', max_length=30, choices=[(b'Aceptado', b'Aceptado'), (b'Rechazado', b'Rechazado'), (b'Pendiente', b'Pendiente'), (b'No Notificado', b'No Notificado'), (b'Cancelado', b'Cancelado')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='work',
            name='userCreator',
            field=models.ForeignKey(verbose_name=b'Creador', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='acceptance',
            name='accepted',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='area',
            name='type',
            field=models.CharField(default=b'Interno', max_length=20, choices=[(b'Interno', b'Interno'), (b'Phone', b'Externo')]),
            preserve_default=True,
        ),
    ]
