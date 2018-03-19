from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
import math

@view_function
def process_request(request, id:int=1):
    product = cmod.Product.objects.get(id=id)
    request.lastFive.insert(0, product)
    print(request.lastFive)
    context = {
        'product' : product ,
    }
    return request.dmp.render('detail.html', context)