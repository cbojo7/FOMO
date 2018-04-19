from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from django.conf import settings
from catalog import models as cmod
import traceback
from django.core.exceptions import ValidationError

@view_function
def process_request(request, order:cmod.Order):
    
    order.recalculate()

    form = CheckOut(request, order=order)
    form.submit_text = None
    if form.is_valid():
        #form.commit()
        return HttpResponseRedirect('/catalog/thankyou/')

    context = {
        'form' : form,
        'order' : order,
    }
    return request.dmp.render('checkout.html', context)

class CheckOut(Formless):
    def init(self):
        self.fields['address'] = forms.CharField(label='Address')
        self.fields['city'] = forms.CharField(label='City')
        self.fields['state'] = forms.CharField(label='State')
        self.fields['zip'] = forms.CharField(label='Zip')
        self.fields['stripeToken'] = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        
        try:
            stripe_charge_token = self.cleaned_data.get('stripeToken')
            self.order.finalize(stripe_charge_token)
        except Exception as e:
            traceback.print_exc()
            raise forms.ValidationError(e)

        return self.cleaned_data
        
