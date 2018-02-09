from django_mako_plus import view_function, jscontext
from django.conf import settings
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless

@view_function
def process_request(request):
    # process the form
    # if request.method == 'POST':
    #     print(request.POST['comment'], type(request.POST['comment']))
    #     print(request.POST['renewal_date'], type(request.POST['renewal_date']))
    form = TestForm(request)
    
    if form.is_valid():
        print(self.u)
        
        # work of the form - create user, login user, purchase
        return HttpResponseRedirect('/')

    # render the form
    context = {
        'form' : form,
    }
    return request.dmp_render('formtest.html', context)

class TestForm(Formless):
    
    def init(self):
        self.fields['email'] = forms.CharField(label='email')
        self.fields['password'] = forms.DateField(help_text="password")
        self.u = None

    def clean(self):
        self.u = self.cleaned_data.get('email')
        return self.cleaned_data