from django.contrib.auth.decorators import login_required
from django.urls import path

from roberms_admin import views
from roberms_admin.views import PendingMessages, CompletedMessageRequests

app_name = 'roberms_admin'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('clients', views.clients, name='clients'),
    path('sales_people', views.sales_people, name='sales_people'),
    path('add_sales_person', views.add_sales_person, name='add_sales_person'),
    path('assign/client/<int:sales_person_id>', views.assign_client, name='assign_client'),
    path('sales_person_clients/<int:sales_person_id>', views.sales_person_clients, name='sales_person_clients'),
    path('delete/sales/person/<int:person_id>', views.delete_sales_person, name='delete_sales_person'),
    path('activate_deactivate_sales_person/<int:person_id>', views.activate_deactivate_sales_person, name='activate_deactivate'),

    path('top/ups', views.top_ups, name='top_ups'),
    path('add/top/up', views.add_client_credit, name='add_top_up'),

    path("client/top_ups/<int:client_id>", views.client_top_ups, name='client_top_ups'),

    path('mark_commission_paid/<int:top_up_id>', views.mark_commission_paid, name='mark_commission_paid'),
    path('account/usage', views.account_usage, name='account_usage'),

    #dummy
    path('sample/images', views.client_images, name='client_images'),

    path('change/sender_id/<int:client_id>', views.client_edit, name='customer_edit'),

    path('sales/people/list', views.list_sales_people, name='list_sales_people'),
    path('sales/person/companies/<int:sales_person_id>', views.sales_person_companies, name='sales_person_companies'),
    path('company/appointments/<int:company_id>', views.company_appointments, name='company_appointments'),

    path('pending/messages', views.pending_messages, name='pending_messages'),
    path('completed/messages', views.completed_message_requests, name='completed_message_requests'),
    path('pending/messages/json', login_required(PendingMessages.as_view()), name='pending_messages_json'),
    path('complated/messages/json', login_required(CompletedMessageRequests.as_view()), name='completed_messages_json'),

    path('processes', views.get_supervisor_processes, name='get_processes'),
    path('start/supervisor', views.start_supervisor, name='start_supervisor'),
    path('restart/supervisor', views.restart_supervisor, name='restart_supervisor'),
    path('stop/supervisor', views.stop_supervisor, name='stop_supervisor'),
    path('start/process/<str:process_name>', views.start_process, name='start_process'),
    path('restart/process/<str:process_name>', views.restart_process, name='restart_process'),
    path('stop/process/<str:process_name>', views.stop_process, name='stop_process'),

    path('clean/client/contacts', views.clean_clients, name="clean_clients"),
    path('clean/client/contacts/<int:client_id>', views.clean_client_contacts, name="clean_client_contacts"),
    path('clean/contacts/state/<str:task_id>', views.clean_contacts_state, name="clean_contacts_state"),
    path('poll_contact_update_state/<str:task_id>', views.poll_contact_update_state, name='poll_contact_update_state'),
]