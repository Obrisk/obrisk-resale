# Generated by Django 2.2.7 on 2019-11-27 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0017_classifiedimages_image_mid_size'),
        ('messager', '0008_auto_20191118_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='classified',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message', to='classifieds.Classified'),
        ),
    ]
