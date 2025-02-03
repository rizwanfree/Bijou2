from django.contrib import admin

from .models import Payment, PaymentMethod
# Register your models here.


admin.site.register(PaymentMethod)

admin.site.register(Payment)