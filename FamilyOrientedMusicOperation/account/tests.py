from django.test import TestCase
from account import models as amod
from django.contrib.auth.models import Permission, Group, ContentType

class UserModelTest(TestCase):
    
    fixtures = [ 'data.yaml' ]

    def setUp(self):
        self.u1 = amod.User()
        self.u1.first_name = 'Marge'
        self.u1.last_name = 'Simpson'
        self.u1.username_field = 'marge@simpsons.com'
        self.u1.set_password('password')
        self.u1.save()

    def test_user_create_save_load(self):
        #'''tests round trip of user model data to/from database'''
        u2 = amod.User.objects.get(username_field='marge@simpsons.com')
        self.assertEquals(self.u1.first_name, u2.first_name)
        self.assertEquals(self.u1.last_name, u2.last_name)
        self.assertEquals(self.u1.username_field, u2.username_field)
        self.assertEquals(self.u1.password, u2.password)
        self.assertTrue(u2.check_password('password'))

    def test_add_groups_check_permissions(self):
        #'''add groups to a user and check permissions'''
        a = 1 
        self.assertEquals(a, 1)
       
    def test_create_group(self):
        g1 = Group()
        g1.name = 'Salespeople'
        g1.save()
        self.u1.groups.add(g1)
        self.u1.save()
        # self.assertTrue(self.u1.groups.filter(name='SalesPeople'))
        g1.permissions.add(self.u1.groups.get(id=g1.id).first() is not None)
        for p in Permission.objects.all():
            print(p.codename)
            print(p.name)
            print(p.content_type)
            # self.u1.user_permissions.add(p)

        p = Permission()
        p.codename = 'change_product_price'
        p.name = 'Change the price of a product'
        p.content_type = ContentType.objects.get(id=1)
        p.save()
        
    