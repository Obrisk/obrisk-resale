# Generated by Django 2.2.11 on 2021-01-30 11:51

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0021_auto_20210124_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classifiedorder',
            old_name='user',
            new_name='buyer',
        ),
        migrations.RenameField(
            model_name='classifiedorder',
            old_name='chinese_address',
            new_name='recipient_chinese_address',
        ),
        migrations.AddField(
            model_name='classifiedorder',
            name='buyer_transaction_id',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='classifiedorder',
            name='is_offline',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='classifiedorder',
            name='notes',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='classifiedorder',
            name='recipient_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Full name'),
        ),
        migrations.AddField(
            model_name='classifiedorder',
            name='recipient_phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone number'),
        ),
        migrations.AddField(
            model_name='classifiedorder',
            name='seller_transaction_id',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='classifiedtags',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='classifiedtags',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='taggedclassifieds',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classifieds_taggedclassifieds_tagged_items', to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='taggedclassifieds',
            name='object_id',
            field=models.IntegerField(db_index=True, verbose_name='object ID'),
        ),
    ]
