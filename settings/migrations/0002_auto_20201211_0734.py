# Generated by Django 3.1.1 on 2020-12-11 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultsettingsmodel',
            name='default_client_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='settings.orderclienttypemodel', unique=True, verbose_name='Стандартный тип клиента'),
        ),
        migrations.AlterField(
            model_name='defaultsettingsmodel',
            name='default_order_status_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='settings.orderstatusmodel', unique=True, verbose_name='Стандартный статус заказа'),
        ),
    ]