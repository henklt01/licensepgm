# Generated by Django 3.1.6 on 2021-02-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_contacts', '0016_auto_20210225_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('user', 'user')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('removed', 'removed')], max_length=50, null=True),
        ),
    ]
