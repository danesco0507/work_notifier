# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0011_auto_20150313_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='group',
            field=models.ForeignKey(verbose_name=b'Agrupador de trabajo', to='notifier.WorkGroup'),
            preserve_default=True,
        ),
    ]
