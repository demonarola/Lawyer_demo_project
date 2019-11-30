# Generated by Django 2.2.6 on 2019-11-29 09:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer', '0018_auto_20191109_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyer',
            name='address2',
            field=models.CharField(blank=True, max_length=400, null=True, validators=[django.core.validators.RegexValidator(message='Enter Valid Address2', regex='(^[A-Za-z0-9]+|,| |/|[A-Za-z]+)+[A-Za-z0-9]+|,| |$')]),
        ),
    ]