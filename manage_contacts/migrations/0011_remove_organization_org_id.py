# Generated by Django 3.1.6 on 2021-02-22 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_contacts', '0010_organization_org_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='org_id',
        ),
    ]
