# Generated by Django 3.0.7 on 2020-10-02 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0017_auto_20201002_2352'),
        ('users', '0013_auto_20201002_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personal',
            field=models.ForeignKey(default=55, on_delete=django.db.models.deletion.CASCADE, to='profiles.Personal'),
        ),
    ]