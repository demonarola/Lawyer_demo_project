# Generated by Django 2.2.6 on 2019-11-01 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer', '0009_auto_20191101_0928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review_lawyer',
            old_name='date_of_joining',
            new_name='date',
        ),
    ]
