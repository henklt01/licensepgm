# Generated by Django 3.1.6 on 2021-03-13 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_contacts', '0021_auto_20210313_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitlement',
            name='product_name',
            field=models.CharField(choices=[('AppLoader', 'AppLoader'), ('ScenarioBuilder', 'ScenarioBuilder')], max_length=50, null=True),
        ),
    ]
