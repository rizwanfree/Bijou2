from django.db import models
from django.conf import settings
# Create your models here.



class Payment(models.Model):
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return f"Payment of {self.amount_paid} by {self.tenant.first_name} {self.tenant.last_name} on {self.payment_date}"