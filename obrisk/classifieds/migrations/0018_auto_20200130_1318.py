# Generated by Django 2.2.7 on 2020-01-30 05:18

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('classifieds', '0017_classifiedimages_image_mid_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassifiedTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Classifieds Tag',
                'verbose_name_plural': 'Classifieds Tags',
            },
        ),
        migrations.CreateModel(
            name='TaggedClassifieds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classifieds_taggedclassifieds_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classifieds_taggedclassifieds_items', to='classifieds.ClassifiedTags')),
            ],
            options={
                'verbose_name': 'Classified tag',
                'verbose_name_plural': 'Classified Tags',
            },
        ),
        migrations.AddField(
            model_name='classified',
            name='new_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='classifieds.TaggedClassifieds', to='classifieds.ClassifiedTags', verbose_name='Tags'),
        ),
    ]
