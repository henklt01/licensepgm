# Generated by Django 3.1.6 on 2021-02-24 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_contacts', '0012_auto_20210224_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitlement',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_contacts.organization'),
        ),
    ]
