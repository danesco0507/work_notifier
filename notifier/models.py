from django.db import models
from django.contrib.auth.models import User,Group


# Create your models here.
class Area(models.Model):
    INTERN = 'Interno'
    EXTERN = 'Phone'
    TYPE_CHOICE = ((INTERN, 'Interno'), (EXTERN, 'Externo'))
    name = models.CharField(max_length=50, verbose_name='area_name')
    type = models.CharField(max_length=50, choices=TYPE_CHOICE, default=INTERN)
    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50, verbose_name='department_name')
    def __str__(self):
        return self.name


class Municipality(models.Model):
    department = models.ForeignKey(Department, verbose_name='municipality_department')
    name = models.CharField(max_length=50, verbose_name='municipality')
    def __str__(self):
        return self.name


class Impact(models.Model):
    name = models.CharField(max_length=50, verbose_name='impact')
    def __str__(self):
        return self.name


class Cause(models.Model):
    causeType = models.CharField(max_length=50, verbose_name='cause_type')
    internTimeLapse = models.IntegerField(verbose_name='time_lapse')
    externTimeLapse = models.IntegerField(verbose_name='time_lapse')
    DAYS = 'Dias'
    HOURS = 'Horas'
    TYPE_CHOICE = ((DAYS, 'Dias'),(HOURS, 'Horas'))
    timeLapseType = models.CharField(max_length=50, choices=TYPE_CHOICE, default=HOURS)
    def __str__(self):
        return self.causeType


class Work(models.Model):
    description = models.TextField( verbose_name='work_description')
    justification = models.TextField(verbose_name='work_justification')
    observations = models.TextField(verbose_name='work_observation')
    number = models.CharField(max_length=50, verbose_name='work_number', unique=True)
    ticketArea = models.ForeignKey(Area, unique=False, verbose_name='Area')
    externAreaID = models.CharField(max_length=50, verbose_name='ID Externo', blank=True, null=True)
    department = models.ForeignKey(Department, unique=False, verbose_name='Departamento')
    municipality = models.ForeignKey(Municipality, unique=False, verbose_name='Municipio')
    impact = models.ForeignKey(Impact, unique=False, verbose_name='Impacto')
    ticketCause = models.ForeignKey(Cause, unique=False, verbose_name='Causa')
    initialDate = models.DateTimeField(verbose_name='Fecha Inicial')
    finalDate = models.DateTimeField(verbose_name='Fecha Final')
    outboundDate = models.DateField(verbose_name='Fecha Outbound')
    createdDate = models.DateField(verbose_name='Fecha de Creacion')
    limitResponseDate = models.DateTimeField(verbose_name='Fecha limite de respuesta')
    affectTime = models.TimeField(verbose_name='Tiempo de Afectacion', blank=True, null=True)
    rollbackTime = models.TimeField(verbose_name='Tiempo de Rollback', blank=True, null=True)

    userCreator = models.ForeignKey(User, blank=True, null=True, verbose_name='Creador')

    ACCEPTED = 'Aceptado'
    REJECTED = 'Rechazado'
    PENDANT = 'Pendiente'
    NOT_NOTIFIED = 'No Notificado'
    CANCELED = 'Cancelado'
    TYPE_CHOICE = ((ACCEPTED , 'Aceptado'),(REJECTED , 'Rechazado'), (PENDANT , 'Pendiente'),(NOT_NOTIFIED , 'No Notificado'),(CANCELED , 'Cancelado'))
    state = models.CharField(max_length=50, choices=TYPE_CHOICE, default=NOT_NOTIFIED)
    def __str__(self):
        return self.number


class Acceptance(models.Model):
    work = models.ForeignKey(Work, verbose_name='work_acceptance')
    accepted = models.BooleanField(default=True)
    valid = models.BooleanField(default=True, verbose_name='acceptance_valid')
    token = models.CharField(max_length=255, verbose_name='acceptance_token')
    notifiedDate = models.DateTimeField(blank=True, null=True, verbose_name='notifiedDate')
    responseDate = models.DateTimeField(blank=True, null=True, verbose_name='responseDate')
    nit = models.CharField(max_length=50, blank=True, null=True, verbose_name='acceptance_affected_nit')
    def __str__(self):
        return self.work.number + " - " + self.nit


class Affected(models.Model):
    work = models.ForeignKey(Work, verbose_name='affected_work')
    name = models.CharField(max_length=255, verbose_name='affected_name')
    office = models.CharField(max_length=255, verbose_name='affected_office')
    service = models.CharField(max_length=255, verbose_name='affected_service')
    capacity = models.IntegerField(verbose_name='affected_capacity')
    nit = models.CharField(max_length=50, verbose_name='affected_nit')
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
    nit = models.CharField(max_length=50, verbose_name='client_nit', unique=True)
    segment = models.CharField(max_length=255, verbose_name='client_segment')
    contact = models.CharField(max_length=255, verbose_name='client_contact')
    def __str__(self):
        return self.name + " - " + self.nit


class ClientEmail(models.Model):
    client = models.ForeignKey(Client, verbose_name='client_email')
    email = models.EmailField(verbose_name='email')
    def __str__(self):
        return self.email

