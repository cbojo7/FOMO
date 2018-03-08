from django_mako_plus import view_function, jscontext
from django.conf import settings
from catalog import models as cmod

@view_function

def process_request(request):
    products = cmod.Product.objects.all()
    # render the form
    return request.dmp.render('s1demo.html', {'product' :products[2],})

@view_function
def inner(request):
    return request.dmp.render('s1demo.inner.html', {})