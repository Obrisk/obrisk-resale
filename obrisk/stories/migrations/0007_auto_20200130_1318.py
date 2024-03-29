# Generated by Django 2.2.7 on 2020-01-30 05:18

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('stories', '0006_stories_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Story Tag',
                'verbose_name_plural': 'Story Tags',
            },
        ),
        migrations.AlterField(
            model_name='stories',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', related_name='oldtags', through='stories.TaggedStories', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='TaggedStory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories_taggedstory_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories_taggedstory_items', to='taggit.Tag')),
                ('tags', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='stories.StoryTags')),
            ],
            options={
                'verbose_name': 'Tagged story',
                'verbose_name_plural': 'Tagged stories',
            },
        ),
        migrations.AddField(
            model_name='stories',
            name='new_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='stories.TaggedStory', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
