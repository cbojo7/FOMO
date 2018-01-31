from django.test import TestCase
from account import models as amod

class UserModelTest(TestCase):
    # def setUp(self):
    #     Animal.objects.create(name="lion", sound="roar")
    #     Animal.objects.create(name="cat", sound="meow")

    def test_user_create_save_load(self):
        #'''tests round trip of user model data to/from database'''
        u1 = amod.User()
        u1.first_name = 'Marge'
        u1.last_name = 'Simpson'
        u1.email = 'marge@simpsons.com'
        #u1.password = 'password
        u1.set_password('password')
        u1.save()

        u2 = amod.User.objects.get(u1.email)
        self.assertEquals(u1.first_name, u2.first_name)
        self.assertEquals(u1.last_name, u2.last_name)
        self.assertEquals(u1.email, u2.email)
        self.assertEquals(u1.password, u2.password)
        self.assertTrue(u2.check_password('password'))
