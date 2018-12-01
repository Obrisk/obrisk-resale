# Generated by Django 2.1.3 on 2018-12-01 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0002_auto_20181122_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classified',
            name='content',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='classified',
            name='image',
            field=models.ImageField(upload_to='articles_pictures/%Y/%m/%d/', verbose_name='Featured image'),
        ),
        migrations.AlterField(
            model_name='classified',
            name='status',
            field=models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='P', max_length=1),
        ),
    ]
