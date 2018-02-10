from django_mako_plus import view_function, jscontext
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from django.conf import settings
import re

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
        self.fields['email'] = forms.EmailField(label='Email')
        self.fields['password'] = forms.CharField(label='Password')
        self.fields['password2'] = forms.CharField(label='Confirm Password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        #do your logic


    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long')
        if re.search('\d', password) is None:
            raise forms.ValidationError('Password must contain a number')
        return password

    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data