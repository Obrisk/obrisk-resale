# Generated by Django 2.2.11 on 2020-05-05 08:04

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20200503_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
    ]
