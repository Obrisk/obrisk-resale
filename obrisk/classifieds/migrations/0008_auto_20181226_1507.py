# Generated by Django 2.1.4 on 2018-12-26 07:07

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0007_auto_20181221_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassifiedImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='posts_pictures/%Y/%m/%d/')),
                ('thumb', imagekit.models.fields.ProcessedImageField(upload_to='posts_pictures/%Y/%m/%d/')),
                ('alt', models.CharField(default=uuid.uuid4, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, max_length=70)),
            ],
        ),
        migrations.RemoveField(
            model_name='classified',
            name='district',
        ),
        migrations.RemoveField(
            model_name='classified',
            name='image',
        ),
        migrations.AddField(
            model_name='classified',
            name='displayImage',
            field=imagekit.models.fields.ProcessedImageField(default=None, upload_to='posts_pictures/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='classifiedimages',
            name='classified',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='classifieds.Classified'),
        ),
    ]
