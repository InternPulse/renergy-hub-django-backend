from django.db import models

# Create your models here.
class Sale(models.Model):
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_region = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)