# Generated by Django 2.2.11 on 2021-01-30 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0015_auto_20200505_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storytags',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='storytags',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='taggedstory',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories_taggedstory_tagged_items', to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='taggedstory',
            name='object_id',
            field=models.UUIDField(db_index=True, verbose_name='object ID'),
        ),
    ]
