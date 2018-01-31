from django.db import models
from cuser.models import AbstractCUser


class User(AbstractCUser):
    birthdate = models.DateTimeField(null=True)
    address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    zipcode = models.TextField(null=True, blank=True)
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    username_field = models.TextField(null=True, blank=True)
    password = models.TextField(null=True, blank=True)

    def get_purchases(self):
        return [ 'Roku', 'Apple TV', 'Chromecast']