from django_mako_plus import view_function, jscontext
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from django.conf import settings
import re
from catalog import models as cmod


@view_function
def process_request(request):
    form = SignUp(request)
    
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manage/list/')
    context = {
        'form' : form,
    }
    return request.dmp_render('edit.html', context)

class Edit(Formless):
    
    def init(self):
        name = models.TextField(label='Name')
        description = models.TextField(label='Description')
        category = models.TextField(label='Category')
        price = models.DecimalField(label='Price', max_digits=7, decimal_places=2)
        status = models.TextField(lable='Active')

    def clean(self):
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        category = self.cleaned_data.get('category')
        price = self.cleaned_data.get('price')
        status = self.cleaned_data.get('status')

    def commit(self):
        self.p = cmod.Product()
        self.p.name = self.cleaned_data['name']
        self.p.description = self.cleaned_data['description']
        self.p.category = self.cleaned_data['category']
        self.p.price = self.cleaned_data['price']
        self.p.status = self.cleaned_data['status']
        self.p.save()

