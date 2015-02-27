# Create your views here.
from forms import WorkUploadForm, AcceptanceForm
from models import Affected, Work, WorkPlan, ContingencyPlan, Acceptance, Client
from xlrd import open_workbook, empty_cell
from xlrd.xldate import xldate_as_datetime, xldate_as_tuple
from django.shortcuts import render, get_object_or_404
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.core.mail import EmailMessage
import uuid, datetime
from django.template.loader import get_template
from django.template import Context, Template
from django.views.decorators.cache import never_cache
from django.db.models import Q

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

                try:
                    work = parse_minutegram(book.sheet_by_name('Minutograma TP'), w1)
                    parse_corp_clients(book.sheet_by_name('Clientes Corporativos'), work)
                except IntegrityError as e:
                    messages.error(request, 'Hay un problema con el documento---'+e.message)
    else:
        form = WorkUploadForm()

    workList = Work.objects.all()
    context = {'form': form, 'workList': workList}
    return render(request,'notifier/index.html', context )

@never_cache
def work_view(request, work_id):
    workInstance = get_object_or_404(Work, pk=work_id)
    if request.method == 'POST':
        request = acceptance_creation(request, workInstance)
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


#-----helper functions-----


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
                print "-----"+os.path.join(os.path.dirname(__file__), f)+"-----"
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
                messages.success(request, "mensaje enviado exitosamente a: "+emaildir.email)
            except Exception as e:
                messages.error(request, "Mensaje no enviado a: "+emaildir.email + "   " + e.message)

    return request


def column_value_search(col, value, sheet):
    for i in range(0,sheet.nrows):
        if sheet.cell(i,col).value==value:
            return i


def check_line(line, initial, final, msheet):
    for i in range(initial,final):
        if msheet.cell is empty_cell:
            return False
    return True


def parse_minutegram(msheet, sw):
    work = Work()
    drow = column_value_search(1, 'DESCRIPCION TP:', msheet)
    jrow = column_value_search(1, 'JUSTIFICACION: ', msheet)
    orow = column_value_search(1, 'OBSERVACIONES:', msheet)
    wprow = column_value_search(1, 'PLAN DE TRABAJO (MINUTOGRAMA):', msheet)
    cprow = column_value_search(1, 'PLAN DE CONTINGENCIA / ROLLBACK:', msheet)

    #este bloque de codigo asigna los datos extraidos del formulario al work creado
    work.ticketArea = sw.ticketArea
    work.department = sw.department
    work.municipality = sw.municipality
    work.impact = sw.impact
    work.ticketCause = sw.ticketCause
    work.initialDate = sw.initialDate
    work.finalDate = sw.finalDate
    work.outboundDate = sw.outboundDate
    #-------------------------------------------------------------------------------

    work.description = msheet.cell(drow+1, 1).value
    work.justification = msheet.cell(jrow+1, 1).value
    work.observations = msheet.cell(orow+1, 1).value


    if msheet.cell(0,7).value == '':
        raise IntegrityError.message(msheet.cell(0,7).value)
    else:
        work.number = msheet.cell(0, 7).value


    work.save()

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
    return work



def parse_corp_clients(csheet, work):
    for i in range(3,csheet.nrows):
        if csheet.cell(i,9) is not empty_cell:
            aff = Affected()
            aff.work = work
            aff.name = csheet.cell(i,1).value
            aff.office = csheet.cell(i,3).value
            aff.service = csheet.cell(i,5).value
            aff.capacity = csheet.cell(i,6).value
            aff.nit = int(csheet.cell(i,9).value)

            aff.save()


def get_client_list_by_nit(qList):
    list = []

    for q in qList:
        list.append(Client.objects.get(nit=q.nit))

    return list
