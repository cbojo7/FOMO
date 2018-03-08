from django.db import models
from polymorphic.models import PolymorphicModel
from django.conf import settings

class Category(models.Model):
    # CATEGORY_CHOICES = (
    #     ('instrument', 'Instrument'),
    #     ('sheet_music', 'Sheet Music'),
    #     ('electronics', 'Electronics'),
    #     ('software', 'Software'),
    #     ('lesson_books', 'Lesson Books'),
    # ) 

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

    def image_url(self):
        # do query to get foreign key
        if self.images.all() is None:
            url = settings.STATIC_URL + 'catalog/media/products/notfound.png'
        else:
            url = settings.STATIC_URL + 'catalog/media/products/' + self.images.all().first().filename
        return url
    
    def images_urls(self):
        base_url = settings.STATIC_URL + 'catalog/media/products/'
        image_list = []
        if self.images.all() is None:
            return [ settings.STATIC_URL + 'catalog/media/products/notfound.png' ]
        else:
            for p in self.images.all():
                image_url = base_url + p.filename
                image_list.append(image_url)
            return image_list
        
class BulkProduct(Product):
    TITLE='Bulk'
    quantity = models.IntegerField(default=-1)
    reorder_trigger = models.IntegerField(default=-1)
    reorder_quantity = models.IntegerField(default=-1)
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

class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name="images", on_delete=models.CASCADE)
    filename = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


