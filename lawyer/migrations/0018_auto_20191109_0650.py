# Generated by Django 2.2.6 on 2019-11-09 06:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer', '0017_remove_review_lawyer_sub_practice_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyer',
            name='city',
            field=models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(message='City should only contain letters and mustcontains atleast 2 chracters..', regex='[A-Za-z]{2}[a-z]+$')]),
        ),
    ]
