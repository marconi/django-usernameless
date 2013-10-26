import re

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core import mail

from ..forms import (RegistrationForm,
                     AuthenticationForm,
                     PasswordResetForm,
                     SetPasswordForm)

User = get_user_model()


class TestRegistrationForm(TestCase):
    def test_name_field(self):
        data = {'data': {'name': '',
                         'email': 'alice@wonderland.com',
                         'password': 'secret'},
                'error': ('name', [u'This field is required.'])}
        form = RegistrationForm(data=data['data'])
        self.failIf(form.is_valid())
        self.assertEqual(form.errors[data['error'][0]], data['error'][1])

    def test_unique_email(self):
        # create initial user
        User.objects.create_user('alice', 'alice@wonderland.com', 'secret')

        form = RegistrationForm(data={'name': 'alice',
                                      'email': 'alice@wonderland.com',
                                      'password1': 'secret',
                                      'password2': 'secret'})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['email'], [u'This email is already taken.'])

        form = RegistrationForm(data={'name': 'bob',
                                      'email': 'bob@ong.com',
                                      'password1': 'foo',
                                      'password2': 'foo'})
        self.failUnless(form.is_valid())

    def test_authentication_form(self):
        response = self.client.get(reverse('auth_login'))
        self.failUnless(isinstance(response.context['form'], AuthenticationForm))

    def test_password_reset_form(self):
        response = self.client.get(reverse('auth_password_reset'))
        self.failUnless(isinstance(response.context['form'], PasswordResetForm))

    def test_set_password_form(self):
        # create user first
        raw_user = {'name': 'alice',
                    'email': 'alice@wonderland.com',
                    'password': 'secret'}
        user = User.objects.create_user(**raw_user)

        # request a password reset
        data = {'email': user.email}
        self.client.post(reverse('auth_password_reset'), data=data)

        urlmatch = re.search(r"https?://[^/]*(/.*reset/\S*)", mail.outbox[0].body)
        url = urlmatch.groups()[0]
        response = self.client.get(url)
        self.failUnless(isinstance(response.context['form'], SetPasswordForm))
