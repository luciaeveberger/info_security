# Generated by Django 2.0.5 on 2018-05-30 14:14

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretsmodules', '0003_auto_20180511_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=Decimal('10000.00'), max_digits=20),
        ),
    ]
