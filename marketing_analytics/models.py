from django.db import models

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()  # Adjust based on your schema
    category_id = models.IntegerField()
    name = models.CharField(max_length=255)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_purchased = models.BooleanField(default=False)

    class Meta:
        managed = False  # This prevents Django from managing the table
        db_table = 'cart'
