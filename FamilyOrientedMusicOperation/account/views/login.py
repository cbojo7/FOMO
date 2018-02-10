from django_mako_plus import view_function, jscontext
from django.conf import settings
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless
from django.contrib.auth import authenticate, login
from account import models as amod
import re

@view_function
def process_request(request):

    form = TestForm(request)
    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/account/')

    # render the form
    context = {
        'form' : form,
    }
    return request.dmp_render('login.html', context)

class TestForm(Formless):
    
    def init(self):
        self.fields['email'] = forms.CharField(label='email')
        self.fields['password'] = forms.CharField(help_text="password")
        self.user = None
    
    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if self.user is not None:
            return self.cleaned_data
        else:
            raise forms.ValidationError('Invalid email or password')

    def commit(self):
        login(self.request, self.user)

