from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless

@view_function
def process_request(request):

    return HttpResponseRedirect('/')
