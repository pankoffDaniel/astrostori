# Generated by Django 3.1.1 on 2020-12-12 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_auto_20201211_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultsettingsmodel',
            name='starmap_time',
            field=models.TimeField(default='18:20', verbose_name='Время звездного неба'),
            preserve_default=False,
        ),
    ]