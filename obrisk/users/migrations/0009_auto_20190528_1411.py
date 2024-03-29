# Generated by Django 2.1.7 on 2019-05-28 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190507_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='snapchat_account',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Snapchat profile'),
        ),
        migrations.AlterField(
            model_name='user',
            name='facebook_account',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Facebook profile'),
        ),
        migrations.AlterField(
            model_name='user',
            name='instagram_account',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Instagram account'),
        ),
        migrations.AlterField(
            model_name='user',
            name='linkedin_account',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='LinkedIn profile'),
        ),
    ]
