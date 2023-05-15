# Generated by Django 2.2.4 on 2020-03-18 08:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0028_auto_20200318_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inbox',
            name='phone_number',
            field=models.CharField(default='254704976963', max_length=250),
            preserve_default=False,
        ),
    ]
