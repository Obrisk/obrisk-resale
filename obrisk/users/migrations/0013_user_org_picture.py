# Generated by Django 2.1.7 on 2019-08-09 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20190708_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='org_picture',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
