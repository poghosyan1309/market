from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models

from app_account.managers import UserManager


def phone_validate(value):
    if len(value) != 13:
        raise ValidationError('phone must be 13 characters')

    if not value.startswith('+374'):
        raise ValidationError('phone must start with "+374"')


class User(AbstractBaseUser):
    DoesNotExist = None
    phone = models.CharField(
        max_length=13,
        unique=True,
        validators=[phone_validate],
    )
    name = models.CharField(max_length=150)
    register_date = models.DateTimeField(null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        if not self.register_date:
            self.register_date = datetime.now()
        super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser
