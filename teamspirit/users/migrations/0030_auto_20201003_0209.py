# Generated by Django 3.0.7 on 2020-10-03 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0029_auto_20201003_0209'),
        ('users', '0029_auto_20201003_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personal',
            field=models.ForeignKey(default=90, on_delete=django.db.models.deletion.CASCADE, to='profiles.Personal'),
        ),
    ]
