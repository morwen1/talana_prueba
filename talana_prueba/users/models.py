from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models 
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.core.validators import RegexValidator

class User(AbstractUser):
    """Default user for talana_prueba."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    contestant_user = models.BooleanField(default=True)
    username = models.CharField(max_length=255 , blank=True)
    verified = models.BooleanField(default=False)
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )


    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone= models.CharField(max_length=17 , validators=[phone_regex] , blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    def __str__(self):
        """Return username."""
        return f"{self.username} , {self.email}"