# Generated by Django 2.1.4 on 2019-01-23 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifieds', '0013_auto_20190123_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classifiedimages',
            name='imageUrl',
            field=models.URLField(default='https://res.cloudinary.com/obrisk/image/upload/v1546075169/samples/ecommerce/accessories-bag.jpg', max_length=500),
        ),
    ]
