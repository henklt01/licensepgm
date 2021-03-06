# Generated by Django 3.1.6 on 2021-03-13 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_contacts', '0019_auto_20210311_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='organization',
            name='org_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='entitlement',
            name='product_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manage_contacts.product'),
        ),
    ]
