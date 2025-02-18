from django.db import models
from django.conf import settings
from django.utils.text import slugify

from accomodations.models import Booking
# Create your models here.




class PaymentMethod(models.Model):
    PAYMENT_CHOICES = [
        ('bank_account', 'Bank Account'),
        ('zelle', 'Zelle'),
        ('venmo', 'Venmo'),
        ('paypal', 'PayPal'),
    ]
    
    name = models.CharField(max_length=50, choices=PAYMENT_CHOICES, unique=True)
    details = models.TextField()
    qr_code = models.ImageField(upload_to='payment_method_qr_codes', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return dict(self.PAYMENT_CHOICES).get(self.name, self.name)  # Get display name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())  # Use the human-readable name
        super().save(*args, **kwargs)



class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id}: ${self.amount} ({self.status})"