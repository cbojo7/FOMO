from django_mako_plus import view_function, jscontext
from django.http import HttpResponseRedirect
from django.conf import settings
from catalog import models as cmod

@view_function
def process_request(request, id:int=0):
    
    prod = cmod.Product.objects.get(id=id)
    prod.status = 'B'
    prod.save()
    
    return HttpResponseRedirect('/manager/list/')

    return request.dmp_render('list.html')
