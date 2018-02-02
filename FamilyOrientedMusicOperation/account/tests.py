from django.test import TestCase
from account import models as amod
from django.contrib.auth.models import Permission, Group, ContentType

class UserModelTest(TestCase):
    
    # fixtures = [ 'data.yaml' ]

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
       
    def test_add_group_test_permissions(self):
        g1 = Group()
        g1.name = 'SalesPeople'
        g1.save()
        self.u1.groups.add(g1)
        self.u1.save()
        self.assertTrue(self.u1.groups.filter(id=g1.id))
        
        g1.permissions.add(Permission.objects.get(id=g1.id))
        p = Permission()
        p.codename = 'change_product_price'
        p.name = 'Change the price of a product'
        p.content_type = ContentType.objects.get(id=1)
        p.save()

        g1.permissions.add(p)
        g1.save()
        #self.assertEquals(self.u1.groups.Permission.filter(codename='change_product_price'), 'change_product_price')

    def test_passwrod(self):
        self.u1.set_password('password')
        self.u1.check_password('password')

    def test_field_change(self):
        self.u1.first_name = 'Homer'
        self.u1.save()
        self.assertEquals(self.u1.first_name, 'Homer')

        self.u1.last_name = 'Homer'
        self.u1.save()
        self.assertEquals(self.u1.last_name, 'Homer')

        self.u1.email = 'Homer@homer.com'
        self.u1.save()
        self.assertEquals(self.u1.email, 'Homer@homer.com')



        
    