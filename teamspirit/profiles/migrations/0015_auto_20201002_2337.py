# Generated by Django 3.0.7 on 2020-10-02 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201002_2239'),
        ('profiles', '0014_auto_20201002_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal',
            name='address',
            field=models.ForeignKey(default=28, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Address'),
        ),
    ]
