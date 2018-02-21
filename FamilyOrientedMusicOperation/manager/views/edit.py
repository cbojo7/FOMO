from django_mako_plus import view_function, jscontext
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from django.conf import settings
import re
from catalog import models as cmod


@view_function
def process_request(request, product:cmod.Product.pid):
    form = Edit(request)
    
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manage/list/')
    context = {
        'form' : form,
    }
    return request.dmp_render('edit.html', context)

class Edit(Formless):
    
    def init(self):
        self.fields['name'] = forms.CharField(label='Name')
        self.fields['description'] = forms.CharField(label='Description')
        self.fields['category'] = forms.CharField(label='Category')
        self.fields['price'] = forms.CharField(label='Price')
        self.fields['status'] = forms.CharField(label='Active')

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

