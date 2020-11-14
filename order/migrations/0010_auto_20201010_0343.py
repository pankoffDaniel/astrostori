# Generated by Django 3.1.1 on 2020-10-10 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20201010_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='starmapordermodel',
            name='latitude',
            field=models.FloatField(blank=True, help_text='Если вводите широту, то и долготу тоже. Пример: 55.75697', null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='starmapordermodel',
            name='longitude',
            field=models.FloatField(blank=True, help_text='Если вводите долготу, то и ширину тоже. Пример: 37.61502', null=True, verbose_name='Долгота'),
        ),
    ]