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
        self.fields['type'] = forms.ChoiceField(choices=cmod.Product.TYPE_CHOICES, label='Product Type')
        self.fields['name'] = forms.CharField(label='Name')
        self.fields['description'] = forms.CharField(label='Description')
        self.fields['category'] = forms.ChoiceField(choices=cmod.Category.CATEGORY_CHOICES, label='Category')
        self.fields['price'] = forms.CharField(label='Price')
        self.fields['status'] = forms.ChoiceField(choices=cmod.Product.STATUS_CHOICES, label='Active')
        self.fields['quantity'] = forms.CharField(label='Quantity')
        self.fields['reorder_trigger'] = forms.CharField(label='Reorder Trigger')
        self.fields['reorder_quantity'] = forms.CharField(label='Reorder Quantity')
        self.fields['max_rental_days'] = forms.CharField(label='Max Rental Days')
        self.fields['retire_date'] = forms.DateField(label='Retire Date')
        self.fields['pid'] = forms.CharField(label='Product ID')

    def clean(self):
        type = self.cleaned_data('type')
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        category = self.cleaned_data.get('category')
        price = self.cleaned_data.get('price')
        status = self.cleaned_data.get('status') 
        quantity = self.cleaned_data.get('quantity') 
        reorder_trigger = self.cleaned_data.get('reorder_trigger') 
        reorder_quantity = self.cleaned_data.get('reorder_quantity') 
        max_rental_days = self.cleaned_data.get('max_rental_days') 
        retire_date = self.cleaned_data.get('reitre_date') 
        pid = self.cleaned_data.get('pid') 

    def commit(self):
        self.p = cmod.Product()
        self.p.type = self.cleaned_data['type']
        self.p.name = self.cleaned_data['name']
        self.p.description = self.cleaned_data['description']
        self.p.category = self.cleaned_data['category']
        self.p.price = self.cleaned_data['price']
        self.p.status = self.cleaned_data['status']
        # if p.type = 'BulkProduct':
        #     self.p.quantity = self.cleaned_data['quantity']
        #     self.p.reorder_trigger = self.cleaned_data['reorder_trigger']
        #     self.p.reorder_quantity = self.cleaned_data['reorder_quantity']
        # if p.type = 'RentalProduct':
        #     self.p.max_rental_days = self.cleaned_data['max_rental_days']
        #     self.p.retire_date = self.cleaned_data['retire_date']
        #     self.p.pid = self.cleaned_data['pid']
        # if p.type = 'IndividualProduct':
        #     self.p.pid = self.cleaned_data['pid']
        self.p.save()

