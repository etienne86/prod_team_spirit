# Generated by Django 3.0.7 on 2020-10-02 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0026_auto_20201003_0046'),
        ('users', '0025_auto_20201003_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personal',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='profiles.Personal'),
        ),
    ]