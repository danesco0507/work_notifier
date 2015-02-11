# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acceptance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=True, verbose_name=b'work_accepted')),
                ('valid', models.BooleanField(default=True, verbose_name=b'acceptance_valid')),
                ('token', models.CharField(max_length=255, verbose_name=b'acceptance_token')),
                ('notifiedDate', models.DateTimeField(null=True, verbose_name=b'notifiedDate', blank=True)),
                ('responseDate', models.DateTimeField(null=True, verbose_name=b'responseDate', blank=True)),
                ('nit', models.CharField(max_length=20, null=True, verbose_name=b'acceptance_affected_nit', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Affected',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'affected_name')),
                ('office', models.CharField(max_length=255, verbose_name=b'affected_office')),
                ('service', models.CharField(max_length=255, verbose_name=b'affected_service')),
                ('capacity', models.IntegerField(verbose_name=b'affected_capacity')),
                ('nit', models.CharField(max_length=20, verbose_name=b'affected_nit')),
                ('acceptance', models.ForeignKey(verbose_name=b'affected_acceptance', blank=True, to='notifier.Acceptance', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'area_name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cause',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('causeType', models.CharField(max_length=20, verbose_name=b'cause_type')),
                ('timeLapse', models.IntegerField(verbose_name=b'time_lapse')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'client_name')),
                ('nit', models.CharField(unique=True, max_length=20, verbose_name=b'client_nit')),
                ('segment', models.CharField(max_length=255, verbose_name=b'client_segment')),
                ('contact', models.CharField(max_length=255, verbose_name=b'client_contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, verbose_name=b'email')),
                ('client', models.ForeignKey(verbose_name=b'client_email', to='notifier.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContingencyPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('initialDate', models.DateTimeField(verbose_name=b'contingency_plan_initial_date')),
                ('finalDate', models.DateTimeField(verbose_name=b'contingency_plan_final_date')),
                ('affectation', models.CharField(max_length=255, verbose_name=b'contingency_plan_affectation')),
                ('activity', models.CharField(max_length=255, verbose_name=b'contingency_plan_activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'department_name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Impact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'impact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'municipality')),
                ('department', models.ForeignKey(verbose_name=b'municipality_department', to='notifier.Department')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(verbose_name=b'work_description')),
                ('justification', models.TextField(verbose_name=b'work_justification')),
                ('observations', models.TextField(verbose_name=b'work_observation')),
                ('number', models.CharField(max_length=20, verbose_name=b'work_number')),
                ('initialDate', models.DateTimeField(verbose_name=b'work_initial_date')),
                ('finalDate', models.DateTimeField(verbose_name=b'work_final_date')),
                ('department', models.ForeignKey(to='notifier.Department')),
                ('impact', models.ForeignKey(to='notifier.Impact')),
                ('municipality', models.ForeignKey(to='notifier.Municipality')),
                ('ticketArea', models.ForeignKey(to='notifier.Area')),
                ('ticketCause', models.ForeignKey(to='notifier.Cause')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('initialDate', models.DateTimeField(verbose_name=b'plan_initial_date')),
                ('finalDate', models.DateTimeField(verbose_name=b'plan_final_date')),
                ('affectation', models.CharField(max_length=255, verbose_name=b'plan_affectation')),
                ('activity', models.CharField(max_length=255, verbose_name=b'plan_activity')),
                ('work', models.ForeignKey(verbose_name=b'related_work_plan', to='notifier.Work')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contingencyplan',
            name='work',
            field=models.ForeignKey(verbose_name=b'work_contingency_plan', to='notifier.Work'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='affected',
            name='work',
            field=models.ForeignKey(verbose_name=b'affected_work', to='notifier.Work'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acceptance',
            name='work',
            field=models.ForeignKey(verbose_name=b'work_acceptance', to='notifier.Work'),
            preserve_default=True,
        ),
    ]
