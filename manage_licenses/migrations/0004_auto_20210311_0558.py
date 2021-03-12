# Generated by Django 3.1.6 on 2021-03-11 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_licenses', '0003_auto_20210228_0838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='license',
            old_name='creator_address',
            new_name='creator_email',
        ),
        migrations.AddField(
            model_name='license',
            name='IP_Host',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='license',
            name='expiration_date',
            field=models.DateTimeField(null=True, verbose_name='Expiration date '),
        ),
        migrations.AddField(
            model_name='license',
            name='is_permanent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='license',
            name='product_grade',
            field=models.CharField(default='standard', max_length=50),
        ),
        migrations.AddField(
            model_name='license',
            name='product_stations',
            field=models.IntegerField(default=10000),
        ),
    ]