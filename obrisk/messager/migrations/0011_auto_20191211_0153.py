# Generated by Django 2.2.7 on 2019-12-10 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messager', '0010_auto_20191211_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
