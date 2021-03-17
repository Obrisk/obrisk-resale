# Generated by Django 2.2.11 on 2020-07-26 05:08

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20200603_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='unverified_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Unverified_phone'),
        ),
    ]
