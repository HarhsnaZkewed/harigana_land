# Generated by Django 5.1.4 on 2024-12-13 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landapp', '0002_districtdetails_make_numberplate_provincedetails_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NumberPlate',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='make',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='model',
        ),
        migrations.DeleteModel(
            name='vehicle_details',
        ),
        migrations.DeleteModel(
            name='vehicle_processed',
        ),
        migrations.DeleteModel(
            name='Vehicle',
        ),
    ]