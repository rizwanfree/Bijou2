from django.db import models
from django_mailbox.models import Message

class EmailAttachment(models.Model):
    email = models.ForeignKey(Message, on_delete=models.CASCADE)
    file = models.FileField(upload_to='email_attachments/')
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size = models.PositiveIntegerField(default=0)  # in bytes

    def __str__(self):
        return self.filename