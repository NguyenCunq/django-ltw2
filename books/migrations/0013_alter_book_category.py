# Generated by Django 4.1.3 on 2022-12-18 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_alter_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Phiêu lưu', 'Phiêu lưu'), ('Kinh dị', 'Kinh dị'), ('Trinh thám', 'Trinh thám'), ('light novel', 'light novel'), ('E-book', 'E-book'), ('Văn học Việt Nam', 'Văn học Việt Nam'), ('Văn học Nước Ngoài', 'Văn học Nước Ngoài')], max_length=200, null=True),
        ),
    ]
