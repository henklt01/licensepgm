# Generated by Django 3.1.6 on 2021-03-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_contacts', '0034_auto_20210328_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitlement',
            name='creation_date',
            field=models.DateField(null=True, verbose_name='Date created '),
        ),
        migrations.AlterField(
            model_name='entitlement',
            name='expiration_date',
            field=models.DateField(null=True, verbose_name='Expiration date '),
        ),
    ]
