from django.db import models, transaction
from django.conf import settings
from django.forms.models import model_to_dict
from polymorphic.models import PolymorphicModel
from decimal import Decimal
from datetime import datetime
import stripe

#######################################################################
###   Products

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
        if self.images.first() is None:
            url = settings.STATIC_URL + 'catalog/media/products/notfound.jpg'
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

#######################################################################
###   Orders

class Order(models.Model):
    '''An order in the system'''
    STATUS_CHOICES = (
        ( 'cart', 'Shopping Cart' ),
        ( 'payment', 'Payment Processing' ),
        ( 'sold', 'Finalized Sale' ),
    )
    order_date = models.DateTimeField(null=True, blank=True)
    name = models.TextField(blank=True, default="Shopping Cart")
    status = models.TextField(choices=STATUS_CHOICES, default='cart', db_index=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    user = models.ForeignKey('account.User', related_name='orders',  on_delete=models.CASCADE)
    # shipping information
    ship_date = models.DateTimeField(null=True, blank=True)
    ship_tracking = models.TextField(null=True, blank=True)
    ship_name = models.TextField(null=True, blank=True)
    ship_address = models.TextField(null=True, blank=True)
    ship_city = models.TextField(null=True, blank=True)
    ship_state = models.TextField(null=True, blank=True)
    ship_zip_code = models.TextField(null=True, blank=True)

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'Order {}: {}: {}'.format(self.id, self.user.get_full_name(), self.total_price)


    def active_items(self, include_tax_item=True):
        '''Returns the active items on this order'''
        # create a query object (filter to status='active')
        tax_item = Product.objects.filter(name='Sales Tax').first()

        active_items = OrderItem.objects.filter(status='active')

        if include_tax_item == False:
            active_items = active_items.exclude(product = tax_item)
        else: 
            self.get_item(product=tax_item, create=True)

        self.recalculate()
        return active_items

        # if self.items.all():
        #     if not include_tax_item:
        #         return self.items.filter(status='active').exclude(product__name='Sales Tax')
        #     else:
        #         return self.items.filter(status='active')

        # if we aren't including the tax item, alter the
        # query to exclude that OrderItem
        # I simply used the product name (not a great choice,
        # but it is acceptable for credit)


    def get_item(self, product, create=False):
        '''Returns the OrderItem object for the given product'''
        item = OrderItem.objects.filter(order=self, product=product).first()
        if item is None and create:
            item = OrderItem.objects.create(order=self, product=product, price=product.price, quantity=0)
        elif create and item.status != 'active':
            item.status = 'active'
            item.quantity = 0
        item.recalculate()
        item.save()
        return item


    def num_items(self):
        '''Returns the number of items in the cart'''
        return sum(self.active_items(include_tax_item=False).values_list('quantity', flat=True))


    def recalculate(self):
        '''
        Recalculates the total price of the order,
        including recalculating the taxable amount.

        Saves this Order and all child OrderLine objects.
        '''

        tax_item = Product.objects.filter(name='Sales Tax').first()
        order_items = OrderItem.objects.filter(order=self, status='active').exclude(product=tax_item)
        
        # iterate the order items (not including tax item) and get the total price
        total_price = 0
        for i in order_items:
        # call recalculate on each item
            i.recalculate()
            total_price += i.extended 

        # update/create the tax order item (calculate at 7% rate)
        tax_item.price = round(Decimal(total_price) * Decimal(0.07), 2)
        tax_item.extended = tax_item.price
        tax_item.save()

        # update the total and save
        self.total_price = round(total_price + tax_item.price, 2)
        self.save()

    def finalize(self, stripe_charge_token):
        '''Runs the payment and finalizes the sale'''
        with transaction.atomic():
            # recalculate just to be sure everything is updated
            self.recalculate()

            # check that all products are available
            order_products = self.active_items(include_tax_item=False)
            for i in order_products:
                if i.TITLE == 'Bulk':
                    if i.quantity > i.product.quantity:
                        raise ValueError('Products unavailable, check quantity available.')
                elif i.quantity == 0:
                    raise ValueError('Product unavailable')

            # contact stripe and run the payment (using the stripe_charge_token)
            charge = stripe.Charge.create(
                amount= int(self.total_price) * 100,
                currency='usd',
                description=self.order,
                source=stripe_charge_token,
            )
           
            # finalize (or create) one or more payment objects
            try:
                stripe_charge = stripe.Charge.create()
            except:
                raise ValueError('charge did not go through')


            # set order status to sold and save the order

            # update product quantities for BulkProducts
            # update status for IndividualProducts


class OrderItem(PolymorphicModel):
    '''A line item on an order'''
    STATUS_CHOICES = (
        ( 'active', 'Active' ),
        ( 'deleted', 'Deleted' ),
    )
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS_CHOICES, default='active', db_index=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    quantity = models.IntegerField(default=0)
    extended = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'OrderItem {}: {}: {}'.format(self.id, self.product.name, self.extended)



    def recalculate(self):
        '''Updates the order item's price, quantity, extended'''
        # update the price if it isn't already set and we have a product
        self.price = self.product.price

        # default the quantity to 1 if we don't have a quantity set
        if self.quantity == 0:
            self.quantity = 1

        # calculate the extended (price * quantity)
        self.extended = self.price * self.quantity

        # save the changes
        self.save()


class Payment(models.Model):
    '''A payment on a sale'''
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2) # max number is 999,999.99
    validation_code = models.TextField(null=True, blank=True)

