# Generated by Django 2.2.5 on 2019-09-19 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0012_classified_priority'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classified',
            options={'ordering': ('-timestamp',), 'verbose_name': 'Classified', 'verbose_name_plural': 'Classifieds'},
        ),
    ]