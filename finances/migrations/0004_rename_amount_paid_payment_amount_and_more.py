# Generated by Django 5.0.11 on 2025-02-18 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accomodations', '0007_booking_status_and_more'),
        ('finances', '0003_alter_paymentmethod_qr_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='amount_paid',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='date_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='payment_method',
            new_name='method',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='description',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_date',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='tenant',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='accomodations.booking'),
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
    ]
