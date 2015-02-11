from django.db import models


# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=20, verbose_name='area_name')
    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=20, verbose_name='department_name')
    def __str__(self):
        return self.name


class Municipality(models.Model):
    department = models.ForeignKey(Department, verbose_name='municipality_department')
    name = models.CharField(max_length=20, verbose_name='municipality')
    def __str__(self):
        return self.name


class Impact(models.Model):
    name = models.CharField(max_length=20, verbose_name='impact')
    def __str__(self):
        return self.name


class Cause(models.Model):
    causeType = models.CharField(max_length=20, verbose_name='cause_type')
    timeLapse = models.IntegerField(verbose_name='time_lapse')
    def __str__(self):
        return self.causeType


class Work(models.Model):
    description = models.TextField( verbose_name='work_description')
    justification = models.TextField(verbose_name='work_justification')
    observations = models.TextField(verbose_name='work_observation')
    number = models.CharField(max_length=20, verbose_name='work_number')
    ticketArea = models.ForeignKey(Area, unique=False)
    department = models.ForeignKey(Department, unique=False)
    municipality = models.ForeignKey(Municipality, unique=False)
    impact = models.ForeignKey(Impact, unique=False)
    ticketCause = models.ForeignKey(Cause, unique=False)
    initialDate = models.DateTimeField(verbose_name='work_initial_date')
    finalDate = models.DateTimeField(verbose_name='work_final_date')
    def __str__(self):
        return self.number


class Acceptance(models.Model):
    work = models.ForeignKey(Work, verbose_name='work_acceptance')
    accepted = models.BooleanField(default=True, verbose_name='work_accepted')
    valid = models.BooleanField(default=True, verbose_name='acceptance_valid')
    token = models.CharField(max_length=255, verbose_name='acceptance_token')
    notifiedDate = models.DateTimeField(blank=True, null=True, verbose_name='notifiedDate')
    responseDate = models.DateTimeField(blank=True, null=True, verbose_name='responseDate')
    nit = models.CharField(max_length=20, blank=True, null=True, verbose_name='acceptance_affected_nit')
    def __str__(self):
        return self.work.number + " - " + self.nit


class Affected(models.Model):
    work = models.ForeignKey(Work, verbose_name='affected_work')
    name = models.CharField(max_length=255, verbose_name='affected_name')
    office = models.CharField(max_length=255, verbose_name='affected_office')
    service = models.CharField(max_length=255, verbose_name='affected_service')
    capacity = models.IntegerField(verbose_name='affected_capacity')
    nit = models.CharField(max_length=20, verbose_name='affected_nit')
    acceptance = models.ForeignKey(Acceptance, blank=True, null=True, verbose_name='affected_acceptance')
    def __str__(self):
        return self.name


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



class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='client_name')
    nit = models.CharField(max_length=20, verbose_name='client_nit', unique=True)
    segment = models.CharField(max_length=255, verbose_name='client_segment')
    contact = models.CharField(max_length=255, verbose_name='client_contact')
    def __str__(self):
        return self.name + " - " + self.nit


class ClientEmail(models.Model):
    client = models.ForeignKey(Client, verbose_name='client_email')
    email = models.EmailField(verbose_name='email')
    def __str__(self):
        return self.email

