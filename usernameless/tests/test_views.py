from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import User


class TestRegistrationViews(TestCase):
    def test_registration_page(self):
        data = {'name': 'alice',
                'email': 'alice@wonderland.com',
                'password1': 'secret',
                'password2': 'secret'}
        response = self.client.post(reverse('registration_register'), data=data)
        self.assertRedirects(response, reverse('registration_complete'))
        self.assertEqual(User.objects.count(), 1)
