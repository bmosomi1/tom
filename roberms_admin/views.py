import json
from xmlrpc.client import ServerProxy

from celery.result import AsyncResult
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django_datatables_view.base_datatable_view import BaseDatatableView
from invoices.models import Client
from roberms_admin.models import Company, Appointment
from sms.models import *
from sms.utils import SDP
from sms.tasks import clean_group_contacts


is_admin = user_passes_test(lambda user: Manager.objects.filter(user_ptr_id=user.id).first() is not None)


def admin_required(view_function):
    return login_required(is_admin(view_function))


@admin_required
def dashboard(request):
    sales_people = SalesPerson.objects.all()
    clients = Customer.objects.all()
    text_messages = Outgoing.objects.all()
    context = {
        'sales_people_count': sales_people.count(),
        'clients_count': clients.count(),
        'contacts_count': Contact.objects.count(),
        'group_count': Group.objects.count()
    }
    return render(request, 'roberms_admin/dashboard.html', context)


@admin_required
def clients(request):
    clients = Customer.objects.filter(is_active=True)
    context = {
        'clients': clients
    }
    return render(request, 'roberms_admin/clients.html', context)


@admin_required
def client_edit(request, client_id):
    customer = Customer.objects.filter(id=client_id).first()
    if request.method == 'POST':
        sender_name = request.POST['sender_name']
        sender_id = request.POST['sender_id']
        access_code = request.POST['access_code']
        customer.service_id = sender_id
        customer.access_code = access_code
        customer.sender_name = sender_name
        customer.save()
        messages.success(request, f'customer {customer.first_name} {customer.last_name} service id and access code updated successfully')
        return redirect('roberms_admin:clients')
    context = {
        'customer': customer
    }
    return render(request, 'roberms_admin/customer_sender_id.html', context)


@admin_required
def sales_people(request):
    sales_people = SalesPerson.objects.all()
    context = {
        'sales_people': sales_people
    }
    return render(request, 'roberms_admin/sales_people.html', context)


@admin_required
def activate_deactivate_sales_person(request, person_id):
    sales_person = SalesPerson.objects.get(id=person_id)
    if sales_person.is_active:
        sales_person.is_active = False
        sales_person.save()
        messages.success(request, 'Sales person deactivated succesfully')
        return redirect('roberms_admin:sales_people')
    else:
        sales_person.is_active = True
        sales_person.save()
        messages.success(request, 'Sales person Activated Successfully')
        return redirect('roberms_admin:sales_people')


@admin_required
def add_sales_person(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        commission = request.POST['commission']
        # password = get_random_string(length=10)
        phone_number = request.POST['phone_number']

        if User.objects.filter(email=email).count() < 1:
            SalesPerson.objects.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password),
                phone_number=phone_number,
                commission=commission,
            )
            print(password)
            messages.success(request, 'Sales Person Added Successfully')
            return redirect("roberms_admin:sales_people")
        else:
            messages.error(request, 'That email has already been registered to this system')
            return redirect("roberms_admin:add_sales_person")
    return render(request, 'roberms_admin/add_sales_person.html')


@admin_required
def delete_sales_person(request, person_id):
    sales_person = SalesPerson.objects.get(id=person_id)
    sales_person.delete()
    messages.success(request, 'Sales Person Deleted Successfully')
    return redirect('roberms_admin:sales_people')


@admin_required
def assign_client(request, sales_person_id):
    sales = Sale.objects.all()
    ids = []
    for sale in sales:
        ids.append(sale.customer_id)

    if request.method == 'POST':
        client_ids = request.POST.getlist('client_ids[]')
        for id in client_ids:
            print(id)
            Sale.objects.create(
                customer_id=id,
                sales_person_id=sales_person_id
            )
        messages.success(request, 'Clients Assigned Successfully')
        return redirect('roberms_admin:dashboard')
    clients = Customer.objects.exclude(id__in=ids)
    context = {
        'clients': clients,
        'sales_person_id': sales_person_id
    }
    return render(request, 'roberms_admin/assign_client.html', context)


@admin_required
def sales_person_clients(request, sales_person_id):
    sales = Sale.objects.filter(sales_person_id=sales_person_id)
    sales_person = SalesPerson.objects.filter(id=sales_person_id).first()
    client_ids = []
    for sale in sales:
        client_ids.append(sale.customer_id)
    clients = Customer.objects.filter(id__in=client_ids)
    context = {
        'clients': clients,
        'sales_person': sales_person
    }
    return render(request, 'roberms_admin/sales_person_clients.html', context)


@admin_required
def client_top_ups(request, client_id):
    top_ups = ManagerTopUp.objects.filter(user_id=client_id)
    context = {
        'top_ups': top_ups
    }
    return render(request, 'roberms_admin/client_top_ups.html', context)


@admin_required
def top_ups(request):
    client_top_ups = ManagerTopUp.objects.all()
    context = {
        'top_ups': client_top_ups
    }
    return render(request, 'roberms_admin/top_ups.html', context)


@admin_required
def add_client_credit(request):

    if request.method == 'POST':
        sms_count = request.POST['sms_count']
        amount = request.POST['amount']
        user_id = request.POST['customer']
        customer = Customer.objects.filter(id=user_id).first()
        customer.credit = customer.credit + float(sms_count)
        customer.save()
        ManagerTopUp.objects.create(
            sms_count=sms_count,
            amount=amount,
            user_id=user_id,
            timestamp=datetime.datetime.now()
        )
        messages.success(request, 'Credit Updated Successfully')
        return redirect('roberms_admin:top_ups')
    else:
        context = {
            'customers': Customer.objects.filter().order_by('username')
        }
        return render(request, 'roberms_admin/add_top_up.html', context)


@admin_required
def mark_commission_paid(request, top_up_id):
    top_up = ManagerTopUp.objects.filter(id=top_up_id).first()
    if top_up is not None:
        client = top_up.user_id
        if top_up.commission_paid == True:
            messages.error(request, 'Commission Already Marked As Payed')
            return redirect("roberms_admin:client_top_ups", client)
        else:
            top_up.commission_paid = True
            top_up.save()
            messages.success(request, 'Commission Marked As Paid')
            return redirect("roberms_admin:client_top_ups", client)


@admin_required
def account_usage(request):
    top_ups = ManagerTopUp.objects.all()
    customers = Customer.objects.all()
    data = []
    # for customer in customers:
    #     data.append(customer.annotate(last_top_up=top_up for top_up in top_ups ))

    context = {
        'customers': customers
    }
    return render(request, 'roberms_admin/credit_usage.html', context)


@admin_required
def list_sales_people(request):
    people = SalesPerson.objects.all()
    context = {
        'people': people
    }
    return render(request, 'company/sales_people.html', context)


@admin_required
def sales_person_companies(request, sales_person_id):
    companies = Company.objects.filter(sales_person_id=sales_person_id)

    context = {
        'companies': companies
    }
    return render(request, 'company/company_list.html', context)


@admin_required
def company_appointments(request, company_id):
    appointments = Appointment.objects.filter(company_id=company_id)

    context = {
        'appointments': appointments
    }
    return render(request, 'company/appointments.html', context)


# def unapproved_clients(request):
#     clients = Customer.objects.filter(is_active=False)
#     context ={
#         'clients': clients
#     }
#     return render(request, 'roberms_admin/unapproved_clients.html', context)


# def activate_client(request, client_id):
#     client = Customer.objects.filter(is_active=False, id=client_id).first()
#     if client is not None:
#         password = get_random_string(length=8)
#         admin = Customer.objects.filter(id=1).first()
#         client.password = password
#         client.is_active = True
#         client.save()
#         invite_message = f"You have been added to Roberms LTD bulk sms platform. " \
#             f"Use the details below to sign in to you account" \
#             f" Email : {client.email}, Password : {password}"
#         sdp = SDP()
#         response = sdp.send_sms_customized(service_id=admin.service_id, recipients=[client.phone_number],
#                                            message=invite_message, sender_code='')
#         print(response.text)
#         messages.success(request, 'Client approval complete')
#         return redirect('roberms_admin:unapproved_clients')
#     else:
#         messages.error(request, 'Client Does Not Exist Or Has Already Been Approved')
#         return redirect('roberms_admin:unapproved_clients')


#dummy

def client_images(request):
    return render(request, 'dummy/show_images.html')


@admin_required
def pending_messages(request):
    return render(request, 'roberms_admin/pending_messages.html')


@admin_required
def completed_message_requests(request):
    return render(request, 'roberms_admin/completed_messages.html')


class PendingMessages(BaseDatatableView):
    model = OutgoingNew
    columns = ['access_code', 'phone_number', 'text_message', 'sent_time',
               'delivery_status', 'request_identifier', 'oc', 'extra_status']
    order_columns = ['access_code', 'phone_number', 'text_message', 'sent_time',
               'delivery_status', 'request_identifier', 'oc', 'extra_status']
    max_display_length = 10

    def get_initial_queryset(self):
        return self.model.objects.all()

    def render_column(self, row, column):
        return super(PendingMessages, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(text_message__icontains=search)|Q(phone_number__icontains=search)|
                           Q(delivery_status__icontains=search)|Q(delivery_status__icontains=search)|
                           Q(request_identifier__icontains=search)|Q(access_code__icontains=search))
        return qs


class CompletedMessageRequests(BaseDatatableView):
    model = OutgoingDone
    columns = ['access_code', 'phone_number', 'text_message', 'sent_time',
               'delivery_status', 'request_identifier', 'oc', 'extra_status']
    order_columns = ['access_code', 'phone_number', 'text_message', 'sent_time',
               'delivery_status', 'request_identifier', 'oc', 'extra_status']
    max_display_length = 10

    def get_initial_queryset(self):
        return self.model.objects.all()

    def render_column(self, row, column):
        return super(CompletedMessageRequests, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(text_message__icontains=search)|Q(phone_number__icontains=search)|
                           Q(delivery_status__icontains=search)|Q(delivery_status__icontains=search)|
                           Q(request_identifier__icontains=search)|Q(access_code__icontains=search))
        return qs


@admin_required
def get_supervisor_processes(request):
    server = ServerProxy('http://localhost:9001/RPC2')
    processes = server.supervisor.getAllProcessInfo()
    supervisor_server_state = server.supervisor.getState()
    context = {
        'processes': processes,
        'server_state': supervisor_server_state['statename']
    }
    return render(request, 'roberms_admin/processes.html', context)


@admin_required
def restart_supervisor(request):
    server = ServerProxy('http://localhost:9001/RPC2')
    server.supervisor.restart()
    messages.success(request, 'Supervisor server restarted')
    redirect('roberms_admin:get_processes')


@admin_required
def stop_supervisor(request):
    server = ServerProxy('http://localhost:9001/RPC2')
    server.supervisor.shutdown()
    supervisor_server_state = server.supervisor.getState()
    context = {
        'server_state': supervisor_server_state['statename']
    }
    messages.success(request, 'Supervisor server stopped')
    return render(request, 'roberms_admin/processes.html', context)


@admin_required
def start_supervisor(request):
    server = ServerProxy('http://localhost:9001/RPC2')
    server.supervisor.start()
    messages.success(request, 'Supervisor server restarted')
    return redirect('roberms_admin:get_processes')


@admin_required
def restart_process(request, process_name):
    server = ServerProxy('http://localhost:9001/RPC2')
    server.supervisor.stopProcess(process_name)
    server.supervisor.startProcess(process_name)
    messages.success(request, f'Process {process_name} restarted')
    return redirect('roberms_admin:get_processes')


@admin_required
def stop_process(request, process_name):
    server = ServerProxy('http://localhost:9001/RPC2')
    server.supervisor.stopProcess(process_name)
    messages.success(request, f'Process {process_name} stopped')
    return redirect('roberms_admin:get_processes')


@admin_required
def start_process(request, process_name):
    server = ServerProxy('http://localhost:9001/RPC2')
    server.supervisor.startProcess(process_name)
    messages.success(request, f'Process {process_name} started')
    return redirect('roberms_admin:get_processes')


@admin_required
def clean_clients(request):
    clients = Customer.objects.all()
    context = {
        'clients': clients,
    }
    return render(request, 'roberms_admin/clean_clients.html', context)


@admin_required
def poll_contact_update_state(request, task_id):
    job = AsyncResult(task_id)
    data = job.result or job.state
    response_data = {
        'state': job.state,
        'details': job.result,
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@admin_required
def clean_client_contacts(request, client_id):
    client = Customer.objects.filter(id=client_id).first()
    groups = Group.objects.filter(customer_id=client_id)

    if request.method == 'POST':
        group = request.POST['group']
        task = clean_group_contacts.delay(group_id=group, client_id=client_id)
        CustomerTask.objects.create(
            customer_id=client_id,
            task_id=task.id
        )
        return redirect('roberms_admin:clean_contacts_state', task.id)
    context = {
        'groups': groups,
        'client': client
    }
    return render(request, 'roberms_admin/clean_contacts.html', context)


@admin_required
def clean_contacts_state(request, task_id):
    context = {
        'task_id': task_id
    }
    return render(request, 'roberms_admin/clean_contacts_status.html', context)