# Generated by Django 3.1.5 on 2021-09-08 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0003_waterclient'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterClientAll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=250)),
                ('msisdn', models.CharField(max_length=250)),
                ('client_number', models.CharField(max_length=250)),
                ('in_num', models.CharField(max_length=250, null=True)),
                ('meter_num', models.CharField(max_length=250, null=True)),
                ('customer_rate', models.CharField(max_length=250, null=True)),
                ('connection_fee', models.CharField(max_length=250, null=True)),
                ('last_meter_reading_date', models.CharField(max_length=250, null=True)),
                ('email_address', models.CharField(max_length=250, null=True)),
                ('court', models.CharField(max_length=250, null=True)),
                ('last_meter_reading', models.CharField(max_length=250, null=True)),
                ('amount_due', models.CharField(max_length=250, null=True)),
                ('units_consumed', models.CharField(max_length=250, null=True)),
                ('last_payment_date', models.CharField(max_length=250, null=True)),
                ('meter_change_date', models.CharField(max_length=250, null=True)),
                ('connection_fee_paid', models.CharField(max_length=250, null=True)),
                ('message', models.CharField(max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Water',
                'verbose_name_plural': 'Waters',
            },
        ),
    ]
