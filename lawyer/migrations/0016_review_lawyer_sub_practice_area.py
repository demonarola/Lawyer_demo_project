# Generated by Django 2.2.6 on 2019-11-06 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer', '0015_auto_20191104_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='review_lawyer',
            name='sub_practice_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lawyer.Sub_practice_area'),
        ),
    ]
