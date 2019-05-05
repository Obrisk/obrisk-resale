# Generated by Django 2.1.7 on 2019-05-04 08:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0007_classifiedimages_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiedimages',
            name='image_medium',
            field=models.CharField(default=django.utils.timezone.now, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classifiedimages',
            name='image_thumb',
            field=models.CharField(default=django.utils.timezone.now, max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classifiedimages',
            name='image',
            field=models.CharField(max_length=300),
        ),
    ]