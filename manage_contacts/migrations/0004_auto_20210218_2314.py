# Generated by Django 3.1.6 on 2021-02-18 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_contacts', '0003_auto_20210218_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitlement',
            name='organization',
            field=models.ManyToManyField(to='manage_contacts.Organization'),
        ),
    ]
