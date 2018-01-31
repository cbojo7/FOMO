from django.contrib import admin
from account import models as amod

admin.site.register(amod.User)