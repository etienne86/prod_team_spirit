# Generated by Django 3.0.7 on 2020-10-02 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_auto_20201002_2346'),
        ('users', '0012_auto_20201002_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Personal'),
        ),
    ]
