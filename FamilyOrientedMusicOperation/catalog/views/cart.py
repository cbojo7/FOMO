from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='/account/login/')
@view_function
def process_request(request):
    user = request.user
    order = cmod.Order.objects.filter(status='cart', user=user).first()

    order_w_tax = order.active_items()
        
    context = {
        'order' : order,
        'order_w_tax' : order_w_tax,
    }

    if len(order.active_items(include_tax_item=False)) == 0:
            return HttpResponseRedirect('/catalog/')

    return request.dmp.render('cart.html', context)