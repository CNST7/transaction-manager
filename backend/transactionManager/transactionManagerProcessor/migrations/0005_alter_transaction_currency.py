# Generated by Django 5.2.3 on 2025-07-04 18:48

import transactionManagerProcessor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactionManagerProcessor', '0004_alter_transaction_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='currency',
            field=models.CharField(choices=transactionManagerProcessor.models._get_currencies, max_length=3),
        ),
    ]
