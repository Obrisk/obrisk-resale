# Generated by Django 2.1.4 on 2019-02-08 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classified',
            name='details',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='classified',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=300, null=True, unique=True),
        ),
    ]
