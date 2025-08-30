from django.db import models

# Create your models here.

class Product_List(models.Model):
    product_name = models.CharField(max_length=250)
    product_price = models.FloatField()
    product_size = models.FloatField() 