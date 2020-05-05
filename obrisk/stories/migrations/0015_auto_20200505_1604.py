# Generated by Django 2.2.11 on 2020-05-05 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0014_stories_images_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='stories',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='stories',
            name='content',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='stories',
            name='video',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
