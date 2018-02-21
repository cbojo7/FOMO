from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod

@view_function
def process_request(request, product:cmod.Product=None):
    # try:
    #    product = cmod.Product.objects.get(id=request.urlparams[0])
    # except:
    #     return HttpResponseRedirect('/')

    context = {

    }
    return request.dmp_render('index.html', context)