# Generated by Django 2.1.7 on 2019-04-17 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0006_classified_contact_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classified',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
