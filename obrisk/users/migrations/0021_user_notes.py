# Generated by Django 2.2.11 on 2020-07-26 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_user_unverified_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notes',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
