# Generated by Django 3.1.1 on 2020-12-12 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20201212_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='starmapordermodel',
            name='date',
            field=models.DateField(verbose_name='Дата звездного неба'),
        ),
    ]
