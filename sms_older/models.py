import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(get_user_model()):
    location = models.CharField(max_length=250, null=True)
    phone_number = models.TextField(null=True)
    #sender_Id = models.CharField(max_length=11, default='ROBERMS')
    access_code = models.CharField(max_length=11, default='ROBERMS_LTD')
    service_id = models.CharField(max_length=50, default="6015152000175328")
    business_name = models.CharField(max_length=100, default="Business Name")
    credit = models.FloatField(default=5.0)
    customer_code = models.IntegerField(null=True)
    sender_name = models.CharField(max_length=250, default='Roberms LTD', null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    @property
    def contact_count(self):
        groups = Group.objects.filter(customer_id=self.id)
        group_ids = []
        for group in groups:
            group_ids.append(group.id)
        contacts = Contact.objects.filter(group_id__in=group_ids)
        return contacts.count()


class SalesPerson(get_user_model()):
    phone_number = models.IntegerField()
    # models.DecimalField(decimal_places=2, max_digits=15)
    commission = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'SalesPerson'
        verbose_name_plural = 'SalesPeople'

    def customers(self):
        sales = Sale.objects.filter(sales_person_id=self.id)
        customers = []
        if sales is not None:
            for sale in sales:
                customers.append(sale.customer)
            return list(set(customers))



class Manager(get_user_model()):
    phone_number = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'


class Sale(BaseModel):
    sales_person = models.ForeignKey(SalesPerson, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Outgoing(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=50, default='68124233232')
    access_code = models.CharField(max_length=50, default='72345')
    phone_number = models.TextField(null=True)
    text_message = models.TextField(max_length=600, null=True)
    track_code = models.CharField(max_length=50, null=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=1000, null=True)
    oc = models.IntegerField(null=True)
    code = models.IntegerField(null=True)
    request_identifier = models.CharField(null=True, max_length=3000)
    extra_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Outgoing'
        verbose_name_plural = 'Outgoings'

    def get_absolute_url(self):
        return reverse('profile')


class OutgoingNew(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=50, default='68124233232')
    access_code = models.CharField(max_length=50, default='ROBERMS_LTD')
    phone_number = models.TextField(null=True)
    text_message = models.TextField(max_length=600, null=True)
    track_code = models.CharField(max_length=50, null=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=1000, null=True)
    oc = models.IntegerField(null=True)
    code = models.IntegerField(null=True)
    request_identifier = models.CharField(null=True, max_length=3000)
    extra_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'OutgoingNew'
        verbose_name_plural = 'OutgoingsNew'

    def get_absolute_url(self):
        return reverse('profile')


class OutgoingApi(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=50, default='6019542000169037')
    unique_identifier = models.CharField(max_length=250, null=True)
    access_code = models.CharField(max_length=50, default='725701')
    dest_msisdn = models.TextField(null=True)
    text_message = models.TextField(max_length=600, null=True)
    track_code = models.CharField(max_length=50, null=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=1000, null=True)
    oc = models.IntegerField(null=True)
    code = models.IntegerField(null=True)
    request_identifier = models.CharField(null=True, max_length=3000)
    extra_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'OutgoingApi'
        verbose_name_plural = 'OutgoingApis'


class OutgoingApiNew(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=50, default='68124233232')
    access_code = models.CharField(max_length=50, default='ROBERMS_LTD')
    phone_number = models.TextField(null=True)
    text_message = models.TextField(max_length=600, null=True)
    track_code = models.CharField(max_length=50, null=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=1000, null=True)
    oc = models.IntegerField(null=True)
    code = models.IntegerField(null=True)
    request_identifier = models.CharField(null=True, max_length=3000)
    unique_identifier = models.CharField(null=True, max_length=3000)
    extra_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'OutgoingApiNew'
        verbose_name_plural = 'OutgoingsApiNew'


class Outgoing1(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=50)
    access_code = models.CharField(max_length=50)
    phone_number = models.TextField(null=True)
    text_message = models.TextField(max_length=600, null=True)
    track_code = models.CharField(max_length=50, null=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=1000, null=True)
    oc = models.IntegerField(null=True)
    code = models.IntegerField(null=True)
    request_identifier = models.CharField(null=True, max_length=3000)
    extra_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Outgoing1'
        verbose_name_plural = 'Outgoing1'

    def get_absolute_url(self):
        return reverse('profile')


class Outgoing2(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_id = models.CharField(max_length=50, default='68124233232')
    access_code = models.CharField(max_length=50, default='72345')
    phone_number = models.TextField(null=True)
    text_message = models.TextField(max_length=600, null=True)
    track_code = models.CharField(max_length=50, null=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=1000, null=True)
    oc = models.IntegerField(null=True)
    code = models.IntegerField(null=True)
    request_identifier = models.CharField(null=True, max_length=3000)
    extra_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Outgoing2'
        verbose_name_plural = 'Outgoings2'

    def get_absolute_url(self):
        return reverse('profile')


class OutgoingDone(models.Model):
    customer_id = models.BigIntegerField()
    service_id = models.CharField(max_length=50, default='68124233232')
    access_code = models.CharField(max_length=50, default='72345')
    phone_number = models.TextField(null=True)
    text_message = models.TextField(max_length=600, null=True)
    track_code = models.CharField(max_length=50, null=True)
    sent_time = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=1000, null=True)
    oc = models.IntegerField(null=True)
    code = models.IntegerField(null=True)
    request_identifier = models.CharField(null=True, max_length=3000)
    extra_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'OutgoingDone'
        verbose_name_plural = 'OutgoingsDone'

    # def get_absolute_url(self):
    #     return reverse('profile')


class Group(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

class WaterNetwork(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Netowrks'
class WaterCustomerNetwork(models.Model):
    #customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Netowrks'




    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Netowrks'
class Contact(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    # first_name = models.CharField(max_length=250)
    # last_name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

class WaterCourt(models.Model):
    network = models.ForeignKey(WaterNetwork, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    # first_name = models.CharField(max_length=250)
    # last_name = models.CharField(max_length=250, null=True)
    location = models.CharField(max_length=250, null=True)
    coverage = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Court'
        verbose_name_plural = 'Courts'

class WaterClients(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    # first_name = models.CharField(max_length=250)
    # last_name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=12)
    is_active = models.BooleanField(default=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
class TobentoTill(models.Model):
    store_number = models.IntegerField()
    till_name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    till_number = models.IntegerField()

class WaterClient(models.Model):
    company_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)
    client_number = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    kra_pin = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class WaterClientAll(models.Model):
    names = models.CharField(max_length=250)
    msisdn = models.CharField(max_length=250)
    client_number = models.CharField(max_length=250)
    id_num = models.CharField(max_length=250, null=True)
    meter_num = models.CharField(max_length=250, null=True)
    customer_rate = models.CharField(max_length=250, null=True)
    connection_fee = models.CharField(max_length=250, null=True)
    last_meter_reading_date = models.CharField(max_length=250, null=True)
    email_address = models.EmailField(max_length=250, null=True)
    court = models.CharField(max_length=250, null=True)
    network = models.CharField(max_length=250, null=True)
    last_meter_reading = models.FloatField(max_length=250, default=0,null=True)
    amount_due = models.FloatField(max_length=250, default=0,null=True)
    units_consumed = models.FloatField(max_length=250, default=0,null=True)
    last_payment_date = models.CharField(max_length=250, null=True)
    meter_change_date = models.CharField(max_length=250, null=True)
    connection_fee_paid = models.FloatField(max_length=250, default=0,null=True)
    message = models.IntegerField(max_length=250, default=0, null=True)
    amount_0= models.FloatField( default=0,null=True)
    amount_1 = models.FloatField(default=0, null=True)
    amount_2 = models.FloatField(default=0, null=True)
    amount_3 = models.FloatField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Water'
        verbose_name_plural = 'Waters'

class WaterConfigtAll(models.Model):
    names = models.CharField(max_length=250)
    msisdn = models.CharField(max_length=250)
    client_number = models.CharField(max_length=250)
    id_num = models.CharField(max_length=250, null=True)
    meter_num = models.CharField(max_length=250, null=True)
    customer_rate = models.CharField(max_length=250, null=True)
    connection_fee = models.CharField(max_length=250, null=True)
    last_meter_reading_date = models.CharField(max_length=250, null=True)
    email_address = models.EmailField(max_length=250, null=True)
    court = models.CharField(max_length=250, null=True)
    network = models.CharField(max_length=250, null=True)
    last_meter_reading = models.FloatField(max_length=250, default=0,null=True)
    amount_due = models.FloatField(max_length=250, default=0,null=True)
    units_consumed = models.FloatField(max_length=250, default=0,null=True)
    last_payment_date = models.CharField(max_length=250, null=True)
    meter_change_date = models.CharField(max_length=250, null=True)
    connection_fee_paid = models.FloatField(max_length=250, default=0,null=True)
    message = models.IntegerField(max_length=250, default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Water'
        verbose_name_plural = 'Waters'

class WaterMeterReadings(models.Model):
    names = models.CharField(max_length=250)
    msisdn = models.CharField(max_length=250)
    account_number = models.CharField(max_length=250)
    id_num = models.CharField(max_length=250, null=True)
    meter_num = models.CharField(max_length=250, null=True)
    customer_rate = models.CharField(max_length=250, null=True)
    reading_type = models.CharField(max_length=250, null=True)
    last_meter_reading_date = models.CharField(max_length=250, null=True)
    comment = models.EmailField(max_length=250, null=True)
    court = models.CharField(max_length=250, null=True)
    network = models.CharField(max_length=250, null=True)
    previous_reading = models.FloatField(max_length=250, default=0,null=True)
    readings = models.FloatField(max_length=250, default=0, null=True)
    amount_from_units = models.FloatField(max_length=250, default=0, null=True)
    credit = models.FloatField(max_length=250, default=0, null=True)
    arrears = models.FloatField(max_length=250, default=0, null=True)
    amount_due = models.FloatField(max_length=250, default=0,null=True)
    payable = models.FloatField(max_length=250, default=0, null=True)
    confirmed = models.IntegerField(max_length=250, default=0, null=True)
    processed = models.IntegerField(max_length=250, default=0, null=True)
    message = models.IntegerField(max_length=250, default=0, null=True)
    units_consumed = models.FloatField(max_length=250, default=0,null=True)
    last_payment_date = models.CharField(max_length=250, null=True)
    meter_change_date = models.CharField(max_length=250, null=True)
    connection_fee_paid = models.FloatField(max_length=250, default=0,null=True)
    read_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'water_meterreading'
        verbose_name_plural = 'water_meterreadings'

class WaterMeterReadingsRaw(models.Model):
    names = models.CharField(max_length=250)
    msisdn = models.CharField(max_length=250)
    readings = models.FloatField(max_length=250, null=True, default=0)
    account_number = models.CharField(max_length=250)
    processed = models.IntegerField(max_length=250, null=True)
    reading_type = models.CharField(max_length=250, null=True)
    read_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'water_meterreading_raw'
        verbose_name_plural = 'water_meterreading_raw'

class WaterSysConf(models.Model):
    standing_charge = models.FloatField(max_length=250,null=True)
    rate = models.FloatField(max_length=250, null=True)
    comment = models.CharField(max_length=250, null=True, default=0)
    account_number = models.CharField(max_length=250)
    processed = models.IntegerField(max_length=250, null=True)
    reading_type = models.CharField(max_length=250, null=True)
    add_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'water_sys_config'
        verbose_name_plural = 'water_sys_config'

class WaterSysConfHist(models.Model):
    standing_charge = models.FloatField(max_length=250,null=True)
    rate = models.FloatField(max_length=250, null=True)
    comment = models.CharField(max_length=250, null=True, default=0)
    account_number = models.CharField(max_length=250)
    processed = models.IntegerField(max_length=250, null=True)
    reading_type = models.CharField(max_length=250, null=True)
    add_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'water_sys_config_hist'
        verbose_name_plural = 'water_sys_config_hist'

class WaterOutbox(models.Model):
    timestamp = models.CharField(max_length=250,null=True)
    user_id = models.IntegerField(null=True)
    dest_msisdn = models.CharField(max_length=250, null=True, default=0)
    text_message = models.CharField(max_length=400)
    sender_name = models.CharField(max_length=250, null=True)
    track_code = models.CharField(max_length=250, null=True)
    client = models.IntegerField( null=True)
    delivery_status=models.CharField(max_length=250, null=True)
    out_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "water_outbox"
        verbose_name = 'water_outbox'
        verbose_name_plural = 'water_outbox'

class WaterSmsOutNetwork(models.Model):
    timestamp = models.CharField(max_length=250,null=True)
    user_id = models.IntegerField(null=True)
    network = models.CharField(max_length=250, null=True, default=0)
    text_message = models.CharField(max_length=400)
    processed = models.IntegerField(max_length=250, null=True)
    client = models.IntegerField( null=True)
    out_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "water_sms_out_network"
        verbose_name = 'water_outbox_network'
        verbose_name_plural = 'water_outbox_network'

class WaterSmsOut(models.Model):
    timestamp = models.CharField(max_length=250,null=True)
    user_id = models.IntegerField(null=True)
    text_message = models.CharField(max_length=400)
    message_length = models.IntegerField(null=True, default=0)
    deducted_units = models.IntegerField(null=True, default=0)
    court = models.CharField(max_length=400,null=True, default=0)
    network = models.CharField(max_length=400,null=True, default=0)
    processed = models.IntegerField(null=True, default=0)
    client = models.IntegerField( null=True)
    out_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "water_sms_out"


class WaterSmsOutCourt(models.Model):
    timestamp = models.CharField(max_length=250,null=True)
    user_id = models.IntegerField(null=True)
    network = models.CharField(max_length=250, null=True, default=0)
    text_message = models.CharField(max_length=400)
    processed = models.IntegerField(max_length=250, null=True)
    client = models.IntegerField( null=True)
    out_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "water_sms_out_court"
        verbose_name = 'water_outbox_network'
        verbose_name_plural = 'water_outbox_network'
class MeterReadings(models.Model):
    names = models.CharField(max_length=250)
    msisdn = models.CharField(max_length=250)
    account_number = models.CharField(max_length=250)
    id_num = models.CharField(max_length=250, null=True)
    meter_num = models.CharField(max_length=250, null=True)
    customer_rate = models.CharField(max_length=250, null=True)
    reading_type = models.CharField(max_length=250, null=True)
    last_meter_reading_date = models.CharField(max_length=250, null=True)
    comment = models.EmailField(max_length=250, null=True)
    court = models.CharField(max_length=250, null=True)
    network = models.CharField(max_length=250, null=True)
    previous_reading = models.FloatField(max_length=250, default=0,null=True)
    readings = models.FloatField(max_length=250, default=0, null=True)
    amount_from_units = models.FloatField(max_length=250, default=0, null=True)
    credit = models.FloatField(max_length=250, default=0, null=True)
    arrears = models.FloatField(max_length=250, default=0, null=True)
    amount_due = models.FloatField(max_length=250, default=0,null=True)
    payable = models.FloatField(max_length=250, default=0, null=True)
    confirmed = models.IntegerField(max_length=250, default=0, null=True)
    processed = models.IntegerField(max_length=250, default=0, null=True)
    message = models.IntegerField(max_length=250, default=0, null=True)
    units_consumed = models.FloatField(max_length=250, default=0,null=True)
    last_payment_date = models.CharField(max_length=250, null=True)
    meter_change_date = models.CharField(max_length=250, null=True)
    connection_fee_paid = models.FloatField(max_length=250, default=0,null=True)
    read_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'water_meterreading'
        verbose_name_plural = 'water_meterreadings'


class WaterMeterReplacement(models.Model):
    client = models.ForeignKey(WaterClientAll, on_delete=models.CASCADE)
    comments = models.CharField(max_length=250)
    last_units = models.CharField(max_length=250)
    names = models.CharField(max_length=250, null=True)
    amount_due = models.CharField(max_length=250, null=True)
    court = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=250, null=True)
    network = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



class WaterPaymentReceived(models.Model):
    client = models.ForeignKey(WaterClientAll, on_delete=models.CASCADE)
    dest_msisdn = models.CharField(max_length=250)
    received_from = models.CharField(max_length=250)
    amount = models.CharField(max_length=250, null=True)
    confirmation_code = models.CharField(max_length=250, null=True)
    account_number = models.CharField(max_length=250, null=True)
    account_name = models.CharField(max_length=250, null=True)
    balance_carried_forward = models.CharField(max_length=250, null=True)
    comments = models.CharField(max_length=250, null=True)
    pay_date = models.DateTimeField(auto_now_add=True)

class WaterPaymentReceivedManual(models.Model):
    client = models.ForeignKey(WaterClientAll, on_delete=models.CASCADE)
    dest_msisdn = models.CharField(max_length=250)
    received_from = models.CharField(max_length=250)
    amount = models.CharField(max_length=250, null=True)
    confirmation_code = models.CharField(max_length=250, null=True)
    account_number = models.CharField(max_length=250, null=True)
    account_name = models.CharField(max_length=250, null=True)
    balance_carried_forward = models.CharField(max_length=250, null=True)
    processed = models.IntegerField(max_length=4, default=0)
    ref_id = models.CharField(max_length=250, null=True)
    comments = models.CharField(max_length=250, null=True)
    pay_date = models.DateTimeField(auto_now_add=True)



class WaterSystemConfig(models.Model):
    standing_charge = models.CharField(max_length=250)
    rate = models.CharField(max_length=250)
    the_changes = models.CharField(max_length=250, null=True)
    user_id = models.CharField(max_length=250, null=True)
    timestamp = models.IntegerField(max_length=4, default=0)
    clients = models.CharField(max_length=250, null=True)
    comments = models.CharField(max_length=250, null=True)
    add_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, default=1, on_delete=models.CASCADE)

class MpesaPayments(BaseModel):
    phone_number = models.IntegerField()
    reference_number = models.CharField(max_length=250)
    amount = models.FloatField()
    till_number = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    verification_code = models.IntegerField
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    verified = models.BooleanField(default=0)


class UserTopUp(BaseModel):
    phone_number = models.CharField(max_length=12)
    transaction_ref = models.IntegerField()
    amount = models.FloatField()
    till_number = models.IntegerField()
    f_name = models.CharField(max_length=250)
    l_name = models.CharField(max_length=250)
    verify_code = models.IntegerField()
    user_id = models.IntegerField(null=True)
    verified = models.BooleanField(default=False)
    timestamp = models.TextField()


class Sms_TopUp(models.Model):
    user_phone = models.CharField(max_length=250)
    transaction_ref = models.CharField(max_length=250, unique=True)
    amount = models.CharField(max_length=250)
    till_number = models.CharField(max_length=250)
    f_name = models.CharField(max_length=250)
    l_name = models.CharField(max_length=250)
    signature = models.CharField(max_length=250)
    account_no = models.CharField(max_length=250)
    transaction_type = models.CharField(max_length=250)
    verifycode = models.CharField(max_length=250)
    user_id = models.IntegerField()
    verified = models.IntegerField(default=0)
    timestamp = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


class ManagerTopUp(models.Model):
    sms_count = models.DecimalField(decimal_places=2, max_digits=15)
    amount = models.CharField(max_length=250)
    user_id = models.IntegerField()
    timestamp = models.CharField(max_length=250)
    commission_paid = models.BooleanField(default=False)


class CustomerTrackCode(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    track_code = models.CharField(max_length=250)
    number_of_messages = models.CharField(max_length=250)


class Till_Numbers(BaseModel):
    till = models.CharField(max_length=250)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()


class CustomerTask(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=250, unique=True)
    status_complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class CustomerSubAccounts(get_user_model()):
    owner = models.ForeignKey(Customer, verbose_name="Owner", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Sub Account'
        verbose_name_plural = 'Sub Accounts'


class From_Willinya(models.Model):
    track_code = models.IntegerField()
    message_cost = models.CharField(max_length=250)


class SenderNameApplication(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sender_name = models.CharField(max_length=11)
    application_date = models.DateField(auto_now_add=True)
    application_status = models.BooleanField(default=False)


class ApplicationContact(models.Model):
    name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)
    application = models.ForeignKey(SenderNameApplication, on_delete=models.CASCADE)


class Tag(models.Model):
    hashtag = models.CharField(max_length=250)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    response = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Inbox(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    message = models.TextField()
    phone_number = models.CharField(max_length=250)
    processed = models.BooleanField(default=False)
    tag = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE)
    pushed = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StAnnPatients(models.Model):
    name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)


