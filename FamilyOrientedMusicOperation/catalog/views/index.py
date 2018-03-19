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
        category_id =  0
    else:
        products = cmod.Product.objects.filter(category=category)
        count = products.count()
        page_count = math.ceil(count/6)
        category_id =  category.id

    categories = cmod.Category.objects.all()
    
    context = {
        'categories' : categories, 
        'category' : category,
        'page_count' : page_count,
        'products' : products[0:6],
        jscontext('category_id') : category_id,
        jscontext('page_count') : page_count,
        jscontext('page') : 1,
    }
    return request.dmp.render('index.html', context)

@view_function
def products(request, category:cmod.Category = None, page:int=1):
    products = cmod.Product.objects.all()

    begin = (page - 1) * 6
    end = (page * 6)

    if category is not None:
        products = products.filter(category__id=category.id)

    products = products[begin:end]
    
    context = {
        'products' : products, 
        jscontext('page') : page,
        'category' : category,
    }
    return request.dmp.render('index.products.html', context)
