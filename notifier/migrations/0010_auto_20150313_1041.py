# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0009_auto_20150305_1016'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(unique=True, max_length=50, verbose_name=b'work_number')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='work',
            name='group',
            field=models.ForeignKey(verbose_name=b'Agrupador de trabajo', blank=True, to='notifier.WorkGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='work',
            name='programmed',
            field=models.CharField(default=b'Programado', max_length=50, choices=[(b'Programado', b'Programado'), (b'Reprogramado', b'Reprogramado')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='work',
            name='number',
            field=models.CharField(max_length=50, verbose_name=b'work_number'),
            preserve_default=True,
        ),
    ]
