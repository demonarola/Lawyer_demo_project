# Generated by Django 2.2.6 on 2019-11-29 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer', '0028_auto_20191129_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyer',
            name='year_admitted',
            field=models.CharField(max_length=128),
        ),
    ]