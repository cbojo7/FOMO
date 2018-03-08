from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
import math

@view_function
def process_request(request, category:cmod.Category = None):
    # c=cmod.Category.objects.get(id=category_id)
    #products = cmod.Product.objects.all()
    if category is None:
        products = cmod.Product.objects.all()
        count = products.count()
        page_count = math.ceil(count/6)
        category_id=  0
    else:
        products = cmod.Product.objects.filter(category=category)
        count = products.count()
        page_count = math.ceil(count/6)
        category_id=  category.id

    categories = cmod.Category.objects.all()
    
    context = {
        'categories' : categories, 
        'category' : category,
        'page_count' : page_count,
    }
    return request.dmp.render('index.html', context)

@view_function
def product(request):
    products = cmod.Product.objects.all()
    context = {
        'products' : products, 
    }
    return request.dmp.render('index.product.html', context)