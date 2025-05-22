# signals.py
import email
import logging
from io import BytesIO
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_mailbox.models import Message
from .models import EmailAttachment

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Message)
def process_attachments(sender, instance, created, **kwargs):
    """
    Process email attachments when a new Message is saved.
    Handles both creation of attachments and cleanup of existing ones.
    """
    if not created or not instance.eml:
        return

    try:
        # Reset position in case the file has been read before
        instance.eml.seek(0)
        msg = email.message_from_binary_file(instance.eml)
        
        # Delete any existing attachments for this email (in case of reprocessing)
        EmailAttachment.objects.filter(email=instance).delete()
        
        # Process each part of the email
        for part in msg.walk():
            if part.get_content_disposition() != 'attachment':
                continue

            filename = part.get_filename()
            if not filename:
                continue

            try:
                content_type = part.get_content_type()
                payload = part.get_payload(decode=True)
                
                if not payload:
                    logger.warning(f"Empty attachment: {filename}")
                    continue

                # Create and save the attachment
                attachment = EmailAttachment(
                    email=instance,
                    filename=filename,
                    content_type=content_type,
                    size=len(payload)
                )
                
                attachment.file.save(
                    filename,
                    BytesIO(payload),
                    save=False
                )
                attachment.save()
                
                logger.info(f"Saved attachment: {filename} ({content_type})")

            except Exception as e:
                logger.error(f"Failed to process attachment {filename}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Failed to process email attachments: {str(e)}")
        raise  # Re-raise if you want the transaction to roll back


# Connect the signal handler
def ready(self):
    from django.apps import apps
    if apps.is_installed('django_mailbox'):
        post_save.connect(process_attachments, sender=Message)