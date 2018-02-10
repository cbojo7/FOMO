from django_mako_plus import view_function, jscontext
from django.conf import settings
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless

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
    return request.dmp_render('formtest.html', context)

class TestForm(Formless):
    
    def init(self):
        self.fields['email'] = forms.CharField(label='email')
        self.fields['password'] = forms.DateField(help_text="password")
        self.user = None
    
    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password')
        return self.cleaned_data

    def commit(self):
        login(self.request, self.user)

