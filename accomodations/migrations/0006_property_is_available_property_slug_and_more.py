# Generated by Django 5.1.3 on 2024-12-23 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accomodations', '0005_property_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='property',
            name='total_rooms',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='room',
            name='number_of_bed',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='room',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='room',
            name='type_of_bed',
            field=models.CharField(choices=[('single', 'Single'), ('double', 'Double'), ('queen', 'Queen'), ('king', 'King')], default=('single', 'Single'), max_length=50),
        ),
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
