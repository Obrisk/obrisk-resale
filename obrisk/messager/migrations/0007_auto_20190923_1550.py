# Generated by Django 2.2.5 on 2019-09-23 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messager', '0006_auto_20190919_2027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversation',
            options={'ordering': ('-timestamp',), 'verbose_name': 'Conversation', 'verbose_name_plural': 'Conversations'},
        ),
    ]