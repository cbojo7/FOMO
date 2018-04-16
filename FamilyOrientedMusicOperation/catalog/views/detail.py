from django.conf import settings
from django_mako_plus import view_function, jscontext
from catalog import models as cmod
from account import models as amod
from django.utils.html import escape
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
import math

@view_function
def process_request(request, id:int=1):
    
    product = cmod.Product.objects.get(id=id)
    request.product = product

    if product in request.lastFive:
        request.lastFive.remove(product)
    else: 
        if len(request.lastFive) > 6:
            request.lastFive.pop()
    request.lastFive.insert(0, product)

    form = AddToCart(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/catalog/cart/')

    context = {
        'product' : product,
        'form' : form ,
    }
    return request.dmp.render('detail.html', context)

class AddToCart(Formless):
    submit_text = 'Add to Cart'

    def init(self):
        self.product = self.request.product
        if self.product.TITLE == 'Bulk':
            item_quantity = 0
            if self.request.user.is_authenticated:
                order = self.request.user.orders.filter(status='cart').first()
                if order:
                    items = order.active_items(include_tax_item=False)
                    item_quantity = item.item_quantity
            QUANTITY_CHOICES = ((x, x)
                for x in range(self.product.quantity - item_quantity + 1))
            self.fields['quantity'] = forms.IntegerField(label='Quantity', min_value=0, max_value=self.product.quantity, widget=forms.Select(choices=QUANTITY_CHOICES))
        else:
            self.fields['quantity'] = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if self.product.TITLE =='Bulk':
            total_quantity = quantity
            if self.request.user.is_authenticated:
                order = self.request.user.order.filter(stauts='cart').first()
                if order:
                    items = order.active_items(include_tax_item=False)
                    if items.filter( product__name=self.product.name ): 
                        item = items.filter(product__name=self.product.name).first()
                        total_quantity = total_quantity + item.quantity
                        item_quantity = item.quantity
            if total_quantity > self.product.quantity:
                raise forms.ValidationError('Please select a quantity less than ' + str(self.product.quantity - item_quantity))
        
        return quantity

    def clean(self):
        if not self.request.user.is_authenticated:
            raise forms.ValidationError('Please sign in to add items to your cart')
    
    def commit(self):
        order_response = cmod.Order.objects.get_or_create(status='cart', user=self.request.user)
        order = order_response[0]
        if order_response[0]:
            order.user = self.request.user
            order.save()
            tax = cmod.OrderItem()
            tax.product = cmod.Product.objects.filter(name='Sales Tax').first()
            tax.quantity = 1
            tax.order = order
            tax.save()

        oi = order.get_item(self.request.product, create=True)
        oi.quantity += self.cleaned_data.get('quantity')
        oi.recalculate()
        order.recalculate()
        order.save()

        oi.save()


