
# before the request:
#    request.session -> Dictionary
#     product_ids = session.get ids from the session
#     products = [ convert list of ids to actual objects]
#     request.last_five = [ product objects ]


# after the request:
#     convert request.last_five -> list of ids
#     set the list of ids into the session

from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
import math

class LastFiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        listFive = request.session.get('last_five', [])
        request.lastFive = []
        for i in listFive:
            try 
            catch:
            product = cmod.Product.objects.get(id=i)
            request.lastFive.insert(0, product)
        listFive.clear()


        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        print(request.lastFive)

        for i in request.lastFive:
            itemId = i.id
            listFive.insert(0, itemId)
        request.session['last_five'] = listFive
        listFive.clear()
        request.lastFive.clear()
        return response