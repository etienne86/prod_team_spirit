# Generated by Django 3.0.7 on 2020-09-08 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20200831_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal',
            name='phone_number',
            field=models.CharField(default='', max_length=20, null=True, verbose_name='Téléphone'),
        ),
    ]
