# Generated by Django 4.1.3 on 2022-12-18 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='image/useravt.png', null=True, upload_to='image'),
        ),
    ]