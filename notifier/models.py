from django.db import models


# Create your models here.
class Work(models.Model):
    description = models.CharField(max_length=255, verbose_name='work_description')
    justification = models.CharField(max_length=255, verbose_name='work_justification')
    observations = models.CharField(max_length=255, verbose_name='work_observation')
    number = models.CharField(max_length=20, verbose_name='work_number')


class Affected(models.Model):
    work = models.ForeignKey(Work, verbose_name='affected_work')
    name = models.CharField(max_length=255, verbose_name='affected_name')
    office = models.CharField(max_length=255, verbose_name='affected_office')
    service = models.CharField(max_length=255, verbose_name='affected_service')
    capacity = models.IntegerField(verbose_name='affected_capacity')
    nit = models.CharField(max_length=20, verbose_name='affected_nit')


class WorkPlan(models.Model):
    work = models.ForeignKey(Work, verbose_name='related_work_plan')
    initialDate = models.DateTimeField(verbose_name='plan_initial_date')
    finalDate = models.DateTimeField(verbose_name='plan_final_date')
    affectation = models.CharField(max_length=255, verbose_name='plan_affectation')
    activity = models.CharField(max_length=255, verbose_name='plan_activity')


class ContingencyPlan(models.Model):
    work = models.ForeignKey(Work, verbose_name='work_contingency_plan')
    initialDate = models.DateTimeField(verbose_name='contingency_plan_initial_date')
    finalDate = models.DateTimeField(verbose_name='contingency_plan_final_date')
    affectation = models.CharField(max_length=255, verbose_name='contingency_plan_affectation')
    activity = models.CharField(max_length=255, verbose_name='contingency_plan_activity')


class Acceptance(models.Model):
    work = models.ForeignKey(Work, verbose_name='work_acceptance')
    affected = models.ForeignKey(Affected, verbose_name='affected_acceptance')
    accepted = models.BooleanField(verbose_name='work_accepted')
    valid = models.BooleanField(verbose_name='acceptance_valid')
    token = models.CharField(max_length=255, verbose_name='acceptance_token')


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='client_name')
    nit = models.CharField(max_length=20, verbose_name='client_nit')
    segment = models.CharField(max_length=255, verbose_name='client_segment')
    contact = models.CharField(max_length=255, verbose_name='client_contact')


class ClientEmail(models.Model):
    client = models.ForeignKey(Client, verbose_name='client_email')
    email = models.EmailField(verbose_name='email')