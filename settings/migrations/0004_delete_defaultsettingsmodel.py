# Generated by Django 3.1.1 on 2020-12-11 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_auto_20201211_0736'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DefaultSettingsModel',
        ),
    ]