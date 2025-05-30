# Generated by Django 5.0.11 on 2025-04-28 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_mailbox', '0009_alter_message_eml'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='email_attachments/')),
                ('filename', models.CharField(max_length=255)),
                ('content_type', models.CharField(max_length=100)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_mailbox.message')),
            ],
        ),
    ]
