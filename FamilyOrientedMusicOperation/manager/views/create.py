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
        return HttpResponseRedirect('/manager/list/')
    context = {
        'form' : form,
    }
    return request.dmp.render('create.html', context)

class Create(Formless):
    
    def init(self):
        self.fields['title'] = forms.ChoiceField(choices=cmod.Product.TYPE_CHOICES, label='Product Type')
        self.fields['name'] = forms.CharField(label='Name')
        self.fields['description'] = forms.CharField(label='Description')
        self.fields['category'] = forms.ModelChoiceField(queryset=cmod.Category.objects.order_by('name').all(), label='Category')
        self.fields['price'] = forms.CharField(label='Price')
        self.fields['status'] = forms.ChoiceField(choices=cmod.Product.STATUS_CHOICES, label='Active')
        self.fields['quantity'] = forms.CharField(label='Quantity', required=False)
        self.fields['reorder_trigger'] = forms.CharField(label='Reorder Trigger', required=False)
        self.fields['reorder_quantity'] = forms.CharField(label='Reorder Quantity', required=False)
        self.fields['max_rental_days'] = forms.CharField(label='Max Rental Days', required=False)
        self.fields['retire_date'] = forms.DateField(label='Retire Date', required=False)
        self.fields['pid'] = forms.CharField(label='Product ID')
    
    # def clean_pid(self):
        # pidCheck = self.cleaned_data.get('pid')
        # if cmod.Product.objects.filter(pid=pidCheck).exists():
        #     raise forms.ValidationError('ProductID already exists')
        # return pidCheck

    def clean(self):
        # name = self.cleaned_data.get('name')
        # description = self.cleaned_data.get('description')
        # category = self.cleaned_data.get('category')
        # price = self.cleaned_data.get('price')
        # status = self.cleaned_data.get('status') 
        # pid = self.cleaned_data.get('pid')
        # quantity = self.cleaned_data.get('quantity')
        # reorder_quantity = self.cleaned_data.get('reorder_quantity') 
        # reorder_trigger = self.cleaned_data.get('reorder_trigger') 
        if self.cleaned_data.get('title') == 'BulkProduct':
            if not self.cleaned_data.get('quantity'):
                 raise forms.ValidationError('Enter Quantity')
            if not self.cleaned_data.get('cleaned_data'):
                 raise forms.ValidationError('Enter Reorder Trigger')
            if not self.cleaned_data.get('cleaned_data'):
                 raise forms.ValidationError('Enter Reorder Quantity')
            
        if self.cleaned_data.get('title') == 'RentalProduct':
            if not self.cleaned_data.get('max_rental_days'):
                raise forms.ValidationError('Enter Rental Days')
            if not self.cleaned_data.get('retire_date'):
                raise forms.ValidationError('Enter Retire Date')
        
    def commit(self):
             
        if self.cleaned_data.get('title') == 'BulkProduct':
            p = cmod.BulkProduct()
            p.quantity = self.cleaned_data['quantity']
            p.reorder_trigger = self.cleaned_data['reorder_trigger']
            p.reorder_quantity = self.cleaned_data['reorder_quantity']
        elif self.cleaned_data.get('title') == 'RentalProduct':
            p = cmod.RentalProduct()
            p.max_rental_days = self.cleaned_data['max_rental_days']
            p.retire_date = self.cleaned_data['retire_date']
            p.pid = self.cleaned_data['pid']
        elif self.cleaned_data.get('title') == 'IndividualProduct':
            p = cmod.IndividualProduct()
            p.pid = self.cleaned_data['pid']

        p.TITLE = self.cleaned_data['title']
        p.name = self.cleaned_data['name']
        p.description = self.cleaned_data['description']
        p.category = self.cleaned_data['category']
        p.price = self.cleaned_data['price']
        p.status = self.cleaned_data['status']
        p.save()

