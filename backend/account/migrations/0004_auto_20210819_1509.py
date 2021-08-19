# Generated by Django 3.2.4 on 2021-08-19 15:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_dummy_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Dummy',
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Username must be Alphanumeric', regex='^[a-zA-Z0-9]*$')]),
        ),
    ]
