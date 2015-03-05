# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0007_auto_20150305_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptance',
            name='nit',
            field=models.CharField(max_length=30, null=True, verbose_name=b'acceptance_affected_nit', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='affected',
            name='nit',
            field=models.CharField(max_length=30, verbose_name=b'affected_nit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='area',
            name='name',
            field=models.CharField(max_length=30, verbose_name=b'area_name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='area',
            name='type',
            field=models.CharField(default=b'Interno', max_length=30, choices=[(b'Interno', b'Interno'), (b'Phone', b'Externo')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cause',
            name='causeType',
            field=models.CharField(max_length=30, verbose_name=b'cause_type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='nit',
            field=models.CharField(unique=True, max_length=30, verbose_name=b'client_nit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=30, verbose_name=b'department_name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='impact',
            name='name',
            field=models.CharField(max_length=30, verbose_name=b'impact'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='municipality',
            name='name',
            field=models.CharField(max_length=30, verbose_name=b'municipality'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='work',
            name='externAreaID',
            field=models.CharField(max_length=30, null=True, verbose_name=b'ID Externo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='work',
            name='number',
            field=models.CharField(unique=True, max_length=30, verbose_name=b'work_number'),
            preserve_default=True,
        ),
    ]
