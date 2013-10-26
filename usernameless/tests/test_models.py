from django.test import TestCase
from django.contrib.sites.models import Site

from registration.models import RegistrationProfile

from ..models import User


class TestUserModel(TestCase):

    raw_user = {'name': 'alice',
                'email': 'alice@wonderland.com',
                'password': 'secret'}

    def test_create_user(self):
        user = User.objects.create_user(**self.raw_user)
        self.failUnless(user)
        self.assertEqual(User.objects.count(), 1)

    def test_create_superuser(self):
        user = User.objects.create_superuser(**self.raw_user)
        self.failUnless(user)
        self.failUnless(user.is_staff)
        self.failUnless(user.is_admin)
        self.failUnless(user.is_superuser)


class TestRegistationManager(TestCase):

    raw_user = {'name': 'alice',
                'email': 'alice@wonderland.com',
                'password': 'secret'}

    def test_create_inactive_user(self):
        data = self.raw_user.copy()
        data.update({'site': Site.objects.get_current()})
        user = RegistrationProfile.objects.create_inactive_user(**data)
        self.failUnless(user)
        self.failIf(user.is_active)

    def test_create_profile(self):
        user = User.objects.create_user(**self.raw_user)
        registration_profile = RegistrationProfile.objects.create_profile(user)
        self.failUnless(registration_profile)
