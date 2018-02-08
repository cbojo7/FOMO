from django_mako_plus import view_function
from django import forms
from django.http import HttpResponseRedirect

@view_function
def process_request(request):
    # process the form
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            # work of the form - create user, login user, purchase
            return HttpResponseRedirect('/')
    else:
        form = TestForm()

    # render the form
    context = {
        'form' : form,
    }
    return request.dmp_render('formtest.html', context)

class TestForm(forms.Form):
    comment = forms.CharField(label='your comment')
    #renewal_date = forms.DateField(help_text="enter date")