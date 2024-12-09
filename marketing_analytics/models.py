from django.db import models

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    category_id = models.IntegerField()
    name = models.CharField(max_length=255)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_purchased = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'cart'

    def __str__(self):
        return self.name

