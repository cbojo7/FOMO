from django.db import models
from polymorphic.models import PolymorphicModel

class Category(models.Model):
    CATEGORY_CHOICES = (
        ('Sheet Music', 'Sheet Music'),
        ('accessories', 'Accessories'),
        ('brass_instrument', 'Brass Instrument'),
        ('woodwind_instrument', 'Woodwind Instrument'),
        ('string_instrument', 'String Instrument'),
        ('percussion_instrument', 'Percussion Instrument')
    )

    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name            


class Product(PolymorphicModel):

    TYPE_CHOICES = (
        ('BulkProduct', 'Bulk Product'),
        ('IndividualProduct', 'Individual Product'),
        ('RentalProduct', 'Rental Product'),
    )
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('B', 'Inactive'),
    )

    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.TextField(choices=STATUS_CHOICES, default='A')
    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def get_quantity(self):
        return 1
        
class BulkProduct(Product):
    TITLE='Bulk'
    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()
    pid = models.TextField(default=1)

    def get_quantity(self):
        return self.quantity

class IndividualProduct(Product):
    TITLE = 'Individual'
    pid = models.TextField()

    def get_quantity(self):
        return 1

class RentalProduct(Product):
    TITLE = 'Rental'
    pid = models.TextField()
    max_rental_days = models.IntegerField(default=0)
    retire_date = models.DateField(null=True, blank=True)

    def get_quantity(self):
        return 1