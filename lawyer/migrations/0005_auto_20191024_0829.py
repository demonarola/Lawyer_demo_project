# Generated by Django 2.2.6 on 2019-10-24 08:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer', '0004_auto_20191024_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyer',
            name='address1',
            field=models.CharField(max_length=400, validators=[django.core.validators.RegexValidator(message='Enter Valid Address1', regex='(^[A-Za-z0-9]+|,| |/|[A-Za-z]+)+[A-Za-z0-9]+|,| |$')]),
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='address2',
            field=models.CharField(max_length=400, validators=[django.core.validators.RegexValidator(message='Enter Valid Address2', regex='(^[A-Za-z0-9]+|,| |/|[A-Za-z]+)+[A-Za-z0-9]+|,| |$')]),
        ),
    ]
