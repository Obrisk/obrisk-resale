# Generated by Django 2.2.9 on 2020-03-12 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0012_stories_user_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='stories',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=300, null=True, unique=True),
        ),
    ]
