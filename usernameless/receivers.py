from .models import create_inactive_user, create_profile


def patch():
    """ Apply patch for django-registration's manager methods. """
    from registration import models
    setattr(models.RegistrationManager,
            'create_inactive_user',
            create_inactive_user)
    setattr(models.RegistrationManager,
            'create_profile',
            create_profile)


patch()
