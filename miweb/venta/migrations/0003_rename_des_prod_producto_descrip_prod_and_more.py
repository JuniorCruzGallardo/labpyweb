# Generated by Django 5.2.3 on 2025-06-26 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0002_producto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='des_prod',
            new_name='descrip_prod',
        ),
        migrations.AlterField(
            model_name='producto',
            name='fec_reg',
            field=models.DateTimeField(),
        ),
    ]
