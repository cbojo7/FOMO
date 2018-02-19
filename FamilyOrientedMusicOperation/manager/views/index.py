from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catelog import models cmod

@view_function
def process_request(request, product:cmod.Product):
    # try:
    #    product = cmod.Product.objects.get(id=request.urlparams[0])
    # except:
    #     return HttpResponseRedirect('/')

    context = {

    }
    return request.dmp.render('index.html', context)