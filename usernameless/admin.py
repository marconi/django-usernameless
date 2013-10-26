from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the
    required fields, plus a repeated password.
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("name", "email")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields
    on the user, but replaces the password field with
    admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User

    def clean_password(self):
        # Regardless of what the user provides, return the
        # initial value. This is done here, rather than on
        # the field, because the field does not have access
        # to the initial value
        return self.initial["password"]


class UserAdmin(UserAdmin):
    # Set the add/modify forms
    add_form = UserCreationForm
    form = UserChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("name", "email", "is_staff", "impersonate_link")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("name", "email")
    ordering = ("name",)
    filter_horizontal = ("groups", "user_permissions",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active",
                                    "is_staff",
                                    "is_superuser",
                                    "groups",
                                    "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",),
                "fields": ("name",
                           "email",
                           "password1",
                           "password2")}),
    )

    def impersonate_link(self, obj):
        return u'<a href="%s">Impersonate</a>' % reverse("impersonate-start",
                                                         args=(obj.id,))
    impersonate_link.allow_tags = True
    impersonate_link.short_description = "impersonate"


# Register the new UserAdmin
admin.site.register(User, UserAdmin)
