# Create your views here.
from django.core import serializers
from django.http import HttpResponse
from forms import WorkUploadForm, AcceptanceForm
from models import Affected, Work, WorkPlan, ContingencyPlan, Acceptance, Client, Cause, Area, Department, Municipality
from xlrd import open_workbook, empty_cell
from xlrd.xldate import xldate_as_datetime, xldate_as_tuple
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import uuid, datetime
from django.template.loader import get_template
from django.template import Context, Template
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.utils import timezone

import os
from email.mime.image import MIMEImage


@never_cache
def import_excel_view(request):

    if request.method == 'POST':
        form = WorkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                w1 = form.save(commit=False)
                input_excel = request.FILES['input_excel']
                book = open_workbook(file_contents=input_excel.read())
                # Lectura de excel
                user = request.user
                try:
                    parse_minutegram(book.sheet_by_name('Minutograma TP'), book.sheet_by_name('Clientes Corporativos'), w1, user)

                except IntegrityError as e:
                    messages.error(request, 'Hay un problema con el documento: '+e.__cause__)
    else:
        form = WorkUploadForm()

    pendantWorkList = Work.objects.filter(initialDate__gt=datetime.datetime.now())
    workList = Work.objects.all()

    if 'ticket' in request.GET and request.GET['ticket'] != '':
        pendantWorkList = pendantWorkList.filter(Q(number__icontains=request.GET['ticket']))
        workList = workList.filter(Q(number__icontains=request.GET['ticket']))
    if 'search_initial' in request.GET and request.GET['search_initial'] != '':
        d = datetime.datetime.strptime(request.GET['search_initial'], '%Y-%m-%d %H:%M')
        pendantWorkList = pendantWorkList.filter(initialDate__gte=d)
        workList = workList.filter(initialDate__gt=d)
    if 'search_final' in request.GET and request.GET['search_final'] != '':
        d = datetime.datetime.strptime(request.GET['search_final'], '%Y-%m-%d %H:%M')
        pendantWorkList = pendantWorkList.filter(initialDate__lte=d)
        workList = workList.filter(initialDate__lte=d)

    querys = request.GET.copy()
    if "p_page" in querys:
        del querys["p_page"]
    if "h_page" in querys:
        del querys["h_page"]


    pPaginator = Paginator(pendantWorkList.order_by('-initialDate'), 10)

    p_page = request.GET.get('p_page')

    try:
        pendantList = pPaginator.page(p_page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pendantList = pPaginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pendantList = pPaginator.page(pPaginator.num_pages)

    hPaginator = Paginator(workList.order_by('-initialDate'), 10)
    h_page = request.GET.get('h_page')
    try:
        historicList = hPaginator.page(h_page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        historicList = hPaginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        historicList = hPaginator.page(hPaginator.num_pages)
    context = {'form': form, 'workList': historicList, 'pWorkList': pendantList, 'queries': querys}
    return render(request,'notifier/index.html', context )

@never_cache
def work_view(request, work_id):
    workInstance = get_object_or_404(Work, pk=work_id)
    if request.method == 'POST':
        with transaction.atomic():
            if 'mail' in request.POST or 'mail.y' in request.POST:
                request = acceptance_creation(request, workInstance)
                redirect('/notifier/')
            elif 'accept' in request.POST or 'accept.y' in request.POST:
                workInstance.state = Work.ACCEPTED
                workInstance.save()
                redirect('/notifier')
            elif 'reject' in request.POST or 'reject.y' in request.POST:
                workInstance.state = Work.REJECTED
                workInstance.save()
                redirect('/notifier/')
            elif 'cancel' in request.POST or 'cancel.y' in request.POST:
                workInstance.state = Work.CANCELED
                for acc in workInstance.acceptance_set.all():
                    acc.valid = False
                    acc.save()
                workInstance.save()
                redirect('/notifier/')

    affectedList = workInstance.affected_set.order_by('nit')
    workPlanList = workInstance.workplan_set.order_by('finalDate')
    contingencyPlanList = workInstance.contingencyplan_set.all()

    context = {'work':workInstance, 'affList':affectedList, 'wpList':workPlanList, 'cpList': contingencyPlanList}
    return render(request, 'notifier/work.html', context)

@never_cache
def accept_view(request, acceptance_token):
    acceptanceInstance = get_object_or_404(Acceptance, token=acceptance_token)
    work = acceptanceInstance.work
    workPlanList = list(work.workplan_set.order_by('finalDate'))
    contingencyPlanList = list(work.contingencyplan_set.order_by('finalDate'))
    affectedList = list(work.affected_set.filter(nit__iexact=acceptanceInstance.nit))
    form = AcceptanceForm(request.POST or None, instance=acceptanceInstance)
    if form.is_valid():
        acc = form.save(commit=False)
        acc.valid = False
        acc.responseDate = datetime.datetime.now()
        acc.save()

    context = {'acceptance':acceptanceInstance, 'form':form, 'work':work, 'wpList':workPlanList, 'cpList': contingencyPlanList, 'affectedList': affectedList}
    return render(request, 'notifier/acceptance.html', context)


@never_cache
def acceptance_state_view(request,work_id):
    workInstance = get_object_or_404(Work, id=work_id)

    acceptedList = workInstance.acceptance_set.filter(Q(accepted=True) & Q(responseDate__isnull=False))
    noAcceptedList = workInstance.acceptance_set.filter(Q(accepted=False) & Q(responseDate__isnull=False))
    pendantList = workInstance.acceptance_set.filter(responseDate=None)

    accepted = get_client_list_by_nit(acceptedList)
    noAccepted = get_client_list_by_nit(noAcceptedList)
    pendant = get_client_list_by_nit(pendantList)

    maxi = max(len(accepted), len(noAccepted), len(pendant))

    aRange = range(maxi - len(accepted))
    nRange = range(maxi - len(noAccepted))
    pRange = range(maxi - len(pendant))

    context = {'work': workInstance, 'acceptedList': accepted, 'noAcceptedList': noAccepted, 'pendantList': pendant, 'aRange': aRange, 'nRange': nRange, 'pRange': pRange}
    return render(request, 'notifier/acceptance_state.html', context)

def municipalities_json_models(request, department):
    current_department = Department.objects.get(pk=department)
    municipalities = Municipality.objects.all().filter(department=current_department)
    json_models = serializers.serialize("json", municipalities)
    return HttpResponse(json_models)


#-----helper functions-----

@transaction.atomic
def acceptance_creation(request, work):

    ids = set(affected.id for affected in work.affected_set.all())

    for id in ids:
        affected = work.affected_set.get(id=id)

        if affected.acceptance is None:
            with transaction.atomic():
                acc = Acceptance()
                acc.work = work
                acc.nit = affected.nit
                acc.token = uuid.uuid4().hex
                acc.save()
                work.state = Work.PENDANT
                work.save()

            for other in work.affected_set.all():
                if other.nit == affected.nit:
                    other.acceptance = acc
                    other.save()


    for acceptance in work.acceptance_set.all():
        client = Client.objects.get(nit=acceptance.nit)
        request = send_notification(request, client, acceptance)

    return request



def send_notification(request, client, acceptance):

    for emaildir in client.clientemail_set.all():
        with transaction.atomic():
            try:
                template = get_template('notifier/email_template.html')
                workPlanList = list(acceptance.work.workplan_set.order_by('finalDate'))
                contingencyPlanList = list(acceptance.work.contingencyplan_set.order_by('finalDate'))
                affectedList = list(acceptance.work.affected_set.filter(nit__iexact=client.nit))
                context = Context({'client': client, 'acceptance': acceptance, 'work': acceptance.work, 'wpList':workPlanList, 'cpList': contingencyPlanList, 'affectedList': affectedList})

                msg = template.render(context=context)

                f='static/image002.jpg'
                fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
                msg_img = MIMEImage(fp.read(), 'jpg')
                fp.close()
                msg_img.add_header('Content-ID', '<image002>')

                email = EmailMessage(subject='NOTIFICACION '+acceptance.work.number, to=[emaildir.email],body=msg, from_email='gestion.epros@gmail.com' )
                email.content_subtype = "html"
                email.attach(msg_img)
                email.send()
                if acceptance.notifiedDate==None:
                    acceptance.notifiedDate = datetime.datetime.now()
                    acceptance.save()
                #messages.success(request, "mensaje enviado exitosamente a: "+emaildir.email)
            except Exception as e:
                messages.error(request, "Mensaje no enviado a: "+emaildir.email + "   " + e.message)

    return request


def column_value_search(col, value, sheet):
    for i in range(0,sheet.nrows):
        if sheet.cell(i,col).value==value:
            return i


def check_line(line, initial, final, msheet):
    for i in range(initial,final):
        if msheet.cell(line, i) is empty_cell:
            return False
    return True

@transaction.atomic
def parse_minutegram(msheet, csheet, sw, user):
    work = Work()

    if msheet.cell(0,7).value == '':
        e = IntegrityError()
        e.__cause__="El trabajo no tiene numero"
        raise e
    else:
        work.number = msheet.cell(0, 7).value

    if column_value_search(1, 'DESCRIPCION TP:', msheet):
        drow = column_value_search(1, 'DESCRIPCION TP:', msheet)
    else:
        e = IntegrityError()
        e.__cause__="El documento no tiene seccion DESCRIPCION TP"
        raise e

    if column_value_search(1, 'JUSTIFICACION: ', msheet):
        jrow = column_value_search(1, 'JUSTIFICACION: ', msheet)
    else:
        e = IntegrityError()
        e.__cause__="El documento no tiene seccion JUSTIFICACION"
        raise e

    if column_value_search(1, 'OBSERVACIONES:', msheet):
        orow = column_value_search(1, 'OBSERVACIONES:', msheet)
    else:
        e = IntegrityError()
        e.__cause__="El documento no tiene seccion OBSERVACIONES"
        raise e

    if column_value_search(1, 'PLAN DE TRABAJO (MINUTOGRAMA):', msheet):
        wprow = column_value_search(1, 'PLAN DE TRABAJO (MINUTOGRAMA):', msheet)
    else:
        e = IntegrityError()
        e.__cause__="El documento no tiene seccion PLAN DE TRABAJO"
        raise e

    if column_value_search(1, 'PLAN DE CONTINGENCIA / ROLLBACK:', msheet):
        cprow = column_value_search(1, 'PLAN DE CONTINGENCIA / ROLLBACK:', msheet)
    else:
        e = IntegrityError()
        e.__cause__="El documento no tiene seccion PLAN DE CONTINGENCIA / ROLLBACK"
        raise e


    #este bloque de codigo asigna los datos extraidos del formulario al work creado
    work.ticketArea = sw.ticketArea
    work.department = sw.department
    work.municipality = sw.municipality
    work.impact = sw.impact
    work.ticketCause = sw.ticketCause
    work.initialDate = sw.initialDate
    work.finalDate = sw.finalDate
    work.outboundDate = sw.outboundDate
    work.createdDate = datetime.date.today()
    work.affectTime = sw.affectTime
    work.rollbackTime = sw.rollbackTime
    now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())

    #Si el tiempo dado para la causa esta en horas se entiende que debe pasarse a areas internas y nunca externas
    if sw.ticketCause.timeLapseType == Cause.HOURS and sw.ticketArea.type == Area.INTERN:
        if now + datetime.timedelta(days=1, hours=sw.ticketCause.internTimeLapse) <= sw.initialDate:
            work.limitResponseDate = now + datetime.timedelta(days=1, hours=sw.ticketCause.internTimeLapse)
        else:
            e = IntegrityError()
            e.__cause__="El tiempo maximo de respuesta de los clientes es mas tarde que la fecha de inicio del trabajo"
            raise e
    elif sw.ticketCause.timeLapseType == Cause.HOURS and sw.ticketArea.type == Area.EXTERN:
        e = IntegrityError()
        e.__cause__="La Causa del ticket no puede asignarse a un area externa"
        raise e
    elif sw.ticketCause.timeLapseType == Cause.DAYS and sw.ticketArea.type == Area.INTERN:
        if now + datetime.timedelta(days=1+sw.ticketCause.internTimeLapse) <= sw.initialDate:
            work.limitResponseDate = now + datetime.timedelta(days=1+sw.ticketCause.internTimeLapse)
        else:
            e = IntegrityError()
            e.__cause__="El tiempo maximo de respuesta de los clientes es mas tarde que la fecha de inicio del trabajo"
            raise e
    elif sw.ticketCause.timeLapseType == Cause.DAYS and sw.ticketArea.type == Area.INTERN:
        if now + datetime.timedelta(days=1+sw.ticketCause.externTimeLapse) <= sw.initialDate:
            work.limitResponseDate = now + datetime.timedelta(days=1+sw.ticketCause.externTimeLapse)
        else:
            e = IntegrityError()
            e.__cause__="El tiempo maximo de respuesta de los clientes es mas tarde que la fecha de inicio del trabajo"
            raise e

    #se asigna el usuario loggeado al trabajo
    if user:
        work.userCreator = user
    #-------------------------------------------------------------------------------

    work.description = msheet.cell(drow+1, 1).value
    work.justification = msheet.cell(jrow+1, 1).value
    work.observations = msheet.cell(orow+1, 1).value

    try:
        work.save()
    except Exception:
        e = IntegrityError()
        e.__cause__="Ya existe un trabajo con ese numero"
        raise e

    #loads work plans
    for i in range(wprow+2,cprow):
        if check_line(i, 2, 6, msheet):
            wp = WorkPlan()
            wp.work=work
            wp.initialDate = xldate_as_datetime(msheet.cell(i, 2).value, 0)
            wp.finalDate = xldate_as_datetime(msheet.cell(i, 3).value, 0)
            wp.affectation = datetime.time(*(xldate_as_tuple(msheet.cell(i, 4).value, 0))[3:])
            wp.activity = msheet.cell(i, 5).value

            wp.save()
        else:
            e = IntegrityError()
            e.__cause__="Alguno de los planes de trabajo tiene un campo vacio"
            raise e

    #loads contingency plans
    for i in range(cprow+2, drow-1):
        if check_line(i, 2, 6, msheet):
            cp = ContingencyPlan()
            cp.work=work
            cp.initialDate = xldate_as_datetime(msheet.cell(i, 2).value, 0)
            cp.finalDate = xldate_as_datetime(msheet.cell(i, 3).value, 0)
            cp.affectation = datetime.time(*(xldate_as_tuple(msheet.cell(i, 4).value, 0))[3:])
            cp.activity = msheet.cell(i, 5).value

            cp.save()
        else:
            e = IntegrityError()
            e.__cause__="Alguno de los planes de contingencia tiene un campo vacio"
            raise e

    parse_corp_clients(csheet, work)


def check_empty_nit(csheet):
    for i in range(3,csheet.nrows):
        if not (isinstance(csheet.cell(i, 9).value, float)):
            return False
    return True

@transaction.atomic
def parse_corp_clients(csheet, work):
    if check_empty_nit(csheet):
        for i in range(3,csheet.nrows):
            aff = Affected()
            aff.work = work
            aff.name = csheet.cell(i, 1).value
            aff.office = csheet.cell(i, 3).value
            aff.service = csheet.cell(i, 5).value
            aff.capacity = csheet.cell(i, 6).value
            aff.nit = int(csheet.cell(i, 9).value)
            aff.save()
    else:
        e = IntegrityError()
        e.__cause__="Uno o mas clientes no tienen nit"
        raise e


def get_client_list_by_nit(qList):
    list = []

    for q in qList:
        list.append(Client.objects.get(nit=q.nit))

    return list
