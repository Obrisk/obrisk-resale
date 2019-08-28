# Generated by Django 2.1.7 on 2019-08-24 01:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classifieds', '0012_classified_priority'),
        ('messager', '0002_auto_20190809_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classified', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversaction', to='classifieds.Classified')),
                ('first_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_conv_user', to=settings.AUTH_USER_MODEL)),
                ('second_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='second_conv_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='attachment',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='has_link',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='img_preview',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]