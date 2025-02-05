from django.db import models
from django.conf import settings
from django.utils.text import slugify
# Create your models here.




class PaymentMethod(models.Model):
    PAYMENT_CHOICES = [
        ('bank_account', 'Bank Account'),
        ('zelle', 'Zelle'),
        ('venmo', 'Venmo'),
        ('paypal', 'PayPal'),
        # Add other payment options here
    ]
    
    name = models.CharField(max_length=50, choices=PAYMENT_CHOICES, unique=True)  # Ensure unique name
    details = models.TextField()  # To store details for each payment method
    qr_code = models.ImageField(upload_to='payment_method_qr_codes/', blank=True, null=True)  # Store QR code image if needed
    slug = models.SlugField(unique=True, blank=True, null=True)  # Unique slug field for URL purposes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} Payment Method"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate a slug from the name if not set
        super().save(*args, **kwargs)



class Payment(models.Model):
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)  # Referencing PaymentMethod
    description = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return f"Payment of {self.amount_paid} by {self.tenant.tenant_profile.first_name} {self.tenant.tenant_profile.last_name} on {self.payment_date} using {self.payment_method.name}"