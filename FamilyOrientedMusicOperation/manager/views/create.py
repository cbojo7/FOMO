from django_mako_plus import view_function, jscontext
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from django.conf import settings
import re
from catalog import models as cmod


@view_function
def process_request(request):
    form = Create(request)
    
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/manage/list/')
    context = {
        'form' : form,
    }
    return request.dmp_render('create.html', context)

class Create(Formless):
    
    def init(self):
        self.fields['type'] = forms.CharField(label='Product Type', choices='TYPE_CHOICES')
        self.fields['name'] = forms.CharField(label='Name')
        self.fields['description'] = forms.CharField(label='Description')
        self.fields['category'] = forms.CharField(label='Category')
        self.fields['price'] = forms.CharField(label='Price')
        self.fields['status'] = forms.CharField(label='Active')
        self.fields['quantity'] = forms.CharField(label='Quantity')
        self.fields['reorder_trigger'] = forms.CharField(label='Reorder Trigger')
        self.fields['reorder_quantity'] = forms.CharField(label='Reorder Quantity')
        self.fields['pid'] = forms.CharField(label='Product ID')

    def clean(self):
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        category = self.cleaned_data.get('category')
        price = self.cleaned_data.get('price')
        status = self.cleaned_data.get('status') 
        quantity = self.cleaned_data.get('quantity') 
        reorder_trigger = self.cleaned_data.get('reorder_trigger') 
        reorder_quantity = self.cleaned_data.get('reorder_quantity') 
        pid = self.cleaned_data.get('pid') 

    def commit(self):
        self.p = cmod.Product()
        self.p.name = self.cleaned_data['name']
        self.p.description = self.cleaned_data['description']
        self.p.category = self.cleaned_data['category']
        self.p.price = self.cleaned_data['price']
        self.p.status = self.cleaned_data['status']
        self.p.quantity = self.cleaned_data['quantity']
        self.p.reorder_trigger = self.cleaned_data['reorder_trigger']
        self.p.reorder_quantity = self.cleaned_data['reorder_quantity']
        self.p.pid = self.cleaned_data['pid']
        self.p.save()

