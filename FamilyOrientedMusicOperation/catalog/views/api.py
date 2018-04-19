from django.conf import settings
from django_mako_plus import view_function
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import permission_required
from formlib import Formless
from catalog import models as cmod
from django import forms

@permission_required('account.user')
@view_function
def process_request(request, category:str='', product:str='', max_price:float=0, page:int=1):
    
    products = cmod.Product.objects.all()
    # form = Search(request)
    # if form.is_valid():
    #     form.commit()

    category = request.GET.get('category', '')
    product = request.GET.get('product', '')
    max_price = request.GET.get('max_price', 0)
    max_price = float(max_price)
    page = request.GET.get('page', 1)
    page = int(page)

    if category != '':
        products = products.filter( category__name__icontains=category )
        print('in category')

    if product != '':
        products = products.filter( name__icontains=product ) 
        print('in product')

    if max_price > 0:
        products = products.filter( price__lt=max_price )
        print('in max_price')

    begin = 6 * (int(page) - 1)
    end = 6 * int(page)

    products = [ {'id': p.id, 'name': p.name, 'category': p.category.name, 'price': str(p.price)} for p in products.order_by('category__name', 'name')]
    if page is not None:
        products = products[begin:end]
    else:
        products = products[0:6]

    context = {
        'products': products,
    }

    return JsonResponse(context)
#     return request.dmp.render('api.html', context)

# class Search(Formless):
#     def init(self):
#         self.fields['category'] = forms.CharField(label='Cateogry')
#         self.fields['products'] = forms.CharField(label='Products')
#         self.fields['max_price'] = forms.CharField(label='max_price')

#     def clean(self):
#         category = self.cleaned_data.get('category')
#         products = self.cleaned_data.get('products')
#         max_price = self.cleaned_data.get('max_price')

#     def commit(self):
#         category = self.category
#         products = self.products
#         max_price = self.max_price
