# Generated by Django 5.1.3 on 2024-12-17 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accomodations', '0008_property_is_available_property_total_rooms'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
