from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect
from formlib import Formless

@view_function
def process_request(request):
    # process the form
    if request.method == 'POST':
        print(request.POST['comment'], type(request.POST['comment']))
        print(request.POST['renewal_date'], type(request.POST['renewal_date']))
    form = TestForm(request)
    if form.is_valid():
        # work of the form - create user, login user, purchase
        return HttpResponseRedirect('/')

    # render the form
    context = {
        'form' : form,
    }
    return request.dmp.render('formtest.html', context)

class TestForm(Formless):
    comment = forms.CharField(label='your comment')
    renewal_date = forms.DateField(help_text="enter date")