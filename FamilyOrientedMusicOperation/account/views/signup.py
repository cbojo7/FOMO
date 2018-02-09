from django_mako_plus import view_function, jscontext
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from django.conf import settings

@view_function
def process_request(request):
    form = SignUp(request)
    if form.is_valid():
        
        #form.commit()
        return HttpResponseRedirect('/account/index/')
    context = {
        'form' : form,
    }
    return request.dmp_render('signup.html', context)

class SignUp(Formless):
    
    def init(self):
        self.fields['firstName'] = forms.CharField(label='First Name')
        self.fields['lastName'] = forms.CharField(label='Last Name')
        self.fields['address'] = forms.CharField(label='Address')
        self.fields['city'] = forms.CharField(label='City')
        self.fields['state'] = forms.CharField(label='State')
        self.fields['zip'] = forms.CharField(label='Zip')
        self.fields['email'] = forms.CharField(label='Email')
        self.fields['password'] = forms.CharField(label='Password')
        self.fields['password1'] = forms.CharField(label='Confirm Password')