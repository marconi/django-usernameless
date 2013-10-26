from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm)

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Row, Column, Submit, HTML

User = get_user_model()


class RegistrationForm(forms.Form):
    """
    Copied from registration.forms.RegistrationForm but
    strip off username and added unique email validation.
    """
    required_css_class = 'required'

    name = forms.CharField(label=_("Name"))
    email = forms.EmailField(label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"))

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(Column('name')),
            Row(Column('email')),
            Row(Column('password1')),
            Row(Column('password2')),
            Row(Column(Submit('submit', _('Submit'))),
                css_class='form-actions'),
        )
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email is already taken."))
        return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class AuthenticationForm(BaseAuthenticationForm):
    def __init__(self, *args, **kwargs):
        reset_url = reverse('auth_password_reset')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(Column('username')),
            Row(Column('password')),
            Row(Column(Submit('submit', _('Login')),
                       css_class='large-2'),
                Column(HTML('<a href="%s" class="forgot-password">Forgot password?</a>' % reset_url),
                       css_class='large-10'),
                css_class='form-actions collapse'),
        )
        super(AuthenticationForm, self).__init__(*args, **kwargs)


class PasswordResetForm(BasePasswordResetForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(Column('email')),
            Row(Column(Submit('submit', _('Submit'))),
                css_class='form-actions'),
        )
        super(PasswordResetForm, self).__init__(*args, **kwargs)


class SetPasswordForm(BaseSetPasswordForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(Column('new_password1')),
            Row(Column('new_password2')),
            Row(Column(Submit('submit', _('Update'))),
                css_class='form-actions'),
        )
        super(SetPasswordForm, self).__init__(*args, **kwargs)
