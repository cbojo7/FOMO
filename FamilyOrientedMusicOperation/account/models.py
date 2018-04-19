from django.db import models
from cuser.models import AbstractCUser
#from django.contrib.auth.models import AbstractUser
from catalog import models as cmod


class User(AbstractCUser):
    birthdate = models.DateTimeField(null=True)
    address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    zipcode = models.TextField(null=True, blank=True)

    def get_purchases(self):
        return [ 'Roku', 'Apple TV', 'Chromecast']

    def get_shopping_cart(self):
        return self.orders.filter(status='cart').first()
