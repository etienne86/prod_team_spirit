# Generated by Django 3.0.7 on 2020-06-09 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20200609_1742'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='is_in_standby',
            new_name='is_inactive',
        ),
    ]