# Generated by Django 2.2.7 on 2019-12-18 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0005_auto_20191031_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='stories',
            name='video',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
