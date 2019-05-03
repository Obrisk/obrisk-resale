# Generated by Django 2.1.7 on 2019-05-03 12:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0006_classified_contact_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiedimages',
            name='image',
            field=models.URLField(default=django.utils.timezone.now, max_length=300),
            preserve_default=False,
        ),
    ]
