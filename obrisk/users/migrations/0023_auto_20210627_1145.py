# Generated by Django 2.2.11 on 2021-06-27 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20210124_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='WechatUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Full name')),
                ('org_picture', models.CharField(blank=True, max_length=150, null=True)),
                ('picture', models.CharField(blank=True, max_length=150, null=True)),
                ('thumbnail', models.CharField(blank=True, max_length=150, null=True)),
                ('gender', models.CharField(blank=True, choices=[('1', 'Male'), ('2', 'Female'), ('0', 'Unknown')], max_length=1, null=True)),
                ('wechat_id', models.CharField(blank=True, max_length=150, null=True)),
                ('wechat_openid', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='wechat_openid')),
                ('wechat_unionid', models.CharField(blank=True, max_length=100, null=True, verbose_name='wechat_unionid')),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('province_region', models.CharField(blank=True, max_length=200, null=True, verbose_name='Province')),
                ('city', models.CharField(max_length=200, verbose_name='City')),
                ('country', models.CharField(default='China', max_length=100, verbose_name='Country')),
                ('notes', models.CharField(blank=True, max_length=1000, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='no_of_events_registered',
        ),
        migrations.RemoveField(
            model_name='user',
            name='no_of_jobs_applied',
        ),
        migrations.RemoveField(
            model_name='user',
            name='no_of_jobs_posted',
        ),
    ]
