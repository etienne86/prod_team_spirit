# Generated by Django 3.0.7 on 2020-08-05 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20200805_0727'),
        ('users', '0006_user_personal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personal',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='profiles.Personal'),
            preserve_default=False,
        ),
    ]
