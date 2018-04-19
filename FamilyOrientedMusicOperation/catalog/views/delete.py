from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from django.http import HttpResponseRedirect


@view_function
def process_request(request, line_item:cmod.OrderItem):
    
    line_item.status = 'deleted'
    line_item.save()

    return HttpResponseRedirect('/catalog/cart/')