from django.db import models


class Product(models):
    product_id = models.IntegerField(null=False)
    product_name = models.TextField(null=False)
    product_category_id = models.IntegerField(null=False)
    product_price = models.DecimalField(null=False)
    product_description = models.TextField(null=False)
    product_quantity = models.IntegerField(null=False)
    product_status = models.TextField(null=False)
    create_date = models.DateTimeField(null=False auto_now_add=True)
    last_modified = models.DateTimeField(null=False auto_now=True)

class Product_category(product):
    product_category_id = models.IntegerField(null=False)
    product_category_name = models.TextField(null=False)