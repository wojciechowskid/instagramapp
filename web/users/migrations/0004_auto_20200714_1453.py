# Generated by Django 3.0.8 on 2020-07-14 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200714_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='long_lived_token',
        ),
        migrations.RemoveField(
            model_name='user',
            name='token_update_date',
        ),
    ]
