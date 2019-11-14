# Generated by Django 2.2.6 on 2019-11-01 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer', '0006_delete_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review_Lawyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=228)),
                ('review', models.CharField(max_length=5000)),
                ('rating', models.CharField(blank=True, max_length=128)),
                ('lawyer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lawyer.Lawyer')),
            ],
            options={
                'verbose_name_plural': 'Review Lawyer',
            },
        ),
    ]