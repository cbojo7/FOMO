from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from django.conf import settings
from catalog import models as cmod

@view_function
def process_request(request):
    form = CheckOut(request)
    
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/catalog/thankyou/)
    context = {
        'form' : form,
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
        cart = self.request.cart
        stripe_charge_token = self.cleaned_data.get('stripeToken')

        try:
            cart.finalize(stripe_charge_token)
        except ValueError as e:
            traceback.print_exc()
            raise forms.ValidationError(e)
        