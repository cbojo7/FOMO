from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@view_function
def process_request(request):
    user = request.user

    if user.order.all():
        order = user.order.filter(STATUS_CHOICES='cart')
    else:
        HttpResponseRedirect(catalog/index)
    context = {
        'order' : order,
    }
    return request.dmp.render('cart.html', context)

def search(name, category)