from django_mako_plus import view_function, jscontext
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from django.conf import settings
import re
from catalog import models as cmod


@view_function
def process_request(request, id:int=0):
    
    prod = cmod.Product.objects.get(id=id)
    #  if prod.TITLE == 'Individual':
    initial = { 'name': prod.name, 'description' : prod.description, 'category': prod.category, 'price': prod.price, 'status': prod.status}
    # elif prod.TITLE == 'Bulk':
    #     initial = { 'name': prod.name, 'description' : prod.description, 'category': prod.category, 'price': prod.price, 'status': prod.status, 'quantity': prod.quantity, 'reorder_trigger': prod.reorder_trigger, 'reorder_quantity': prod.reorder_quantity}
    
    form = Edit(request, initial=initial)
    
    if form.is_valid():
        form.commit(prod)
        return HttpResponseRedirect('/manager/list/')
    context = {
        'form' : form,
    }
    return request.dmp_render('edit.html', context)

class Edit(Formless):
    
    def init(self):
        self.fields['name'] = forms.CharField(label='Name')
        self.fields['description'] = forms.CharField(label='Description')
        self.fields['category'] = forms.ModelChoiceField(queryset=cmod.Category.objects.order_by('name').all(), label='Category')
        self.fields['price'] = forms.CharField(label='Price')
        self.fields['status'] = forms.ChoiceField(choices=cmod.Product.STATUS_CHOICES, label='Status')

    def clean(self):
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        category = self.cleaned_data.get('category')
        price = self.cleaned_data.get('price')
        status = self.cleaned_data.get('status')

    def commit(self, p):
        p.name = self.cleaned_data['name']
        p.description = self.cleaned_data['description']
        p.category = self.cleaned_data['category']
        p.price = self.cleaned_data['price']
        p.status = self.cleaned_data['status']
        p.save()
