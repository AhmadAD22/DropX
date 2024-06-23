import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Client


# class UserModelTestCase(TestCase):
#     def setUp(self):
#         self.User = get_user_model()
        
#     def test_create_user(self):
#         user = self.User.objects.create_user(
#             phone='1234567890',
#             password='password123',
#             fullName='John Doe'
#         )
#         self.assertEqual(user.phone, '1234567890')
#         self.assertTrue(user.check_password('password123'))
#         self.assertEqual(user.fullName, 'John Doe')
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)
#         self.assertTrue(user.is_active)
#         self.assertIsNotNone(user.created_at)
#         self.assertIsNotNone(user.updated_on)
        
#     def test_create_superuser(self):
#         superuser = self.User.objects.create_superuser(
#             phone='9876543210',
#             password='admin123',
#             fullName='Admin User'
#         )
#         self.assertEqual(superuser.phone, '9876543210')
#         self.assertTrue(superuser.check_password('admin123'))
#         self.assertEqual(superuser.fullName, 'Admin User')
#         self.assertTrue(superuser.is_staff)
#         self.assertTrue(superuser.is_superuser)
#         self.assertTrue(superuser.is_active)
#         self.assertIsNotNone(superuser.created_at)
#         self.assertIsNotNone(superuser.updated_on)

class ClientModelTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_client(self):
        client = self.User.objects.create_user(
            phone='1234567890',
            password='password123',
            fullName='John Doe'
        )
        client.avatar = 'path/to/avatar.jpg'
        client.save()

        self.assertEqual(client.avatar, 'path/to/avatar.jpg')
        self.assertEqual(client.fullName, 'John Doe')
        client.delete()
        # Verify that the string representation includes the full name
        # self.assertIn('John Doe', client)

class ClientModelTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_client(self):
        client = self.User.objects.create_user(
            phone='1234567890',
            password='password123',
            fullName='John Doe'
        )
        client.avatar = 'path/to/avatar.jpg'
        client.save()

        self.assertEqual(client.avatar, 'path/to/avatar.jpg')
        self.assertEqual(client.fullName, 'John Doe')
        client.delete()
        client1=Client.objects.all()
        for c in client1:
            c.delete()
        # Verify that the string representation includes the full name
        # self.assertIn('John Doe', client)

if __name__ == '__main__':
    unittest.main()