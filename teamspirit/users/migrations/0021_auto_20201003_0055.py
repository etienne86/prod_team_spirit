# Generated by Django 3.0.7 on 2020-10-02 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0026_auto_20201003_0046'),
        ('users', '0020_auto_20201003_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personal',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='profiles.Personal'),
        ),
    ]