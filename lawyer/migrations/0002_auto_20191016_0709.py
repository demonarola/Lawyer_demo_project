# Generated by Django 2.2.6 on 2019-10-16 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='state_name',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]