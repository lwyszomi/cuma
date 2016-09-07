from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models

from django.utils.translation import ugettext_lazy as _


class DHIS2UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, first_name=None, last_name=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email=None, password=None, first_name=None, last_name=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.set_password(password)
        user.save()
        return user


class DHIS2User(AbstractBaseUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    external_id = models.CharField(_('external id'), max_length=128, unique=True,
                                   db_index=True, null=True, blank=True)

    objects = DHIS2UserManager()

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return u'{} {}'.format(self.first_name or '', self.last_name or '')

    def get_short_name(self):
        return self.get_full_name()

    def has_perm(self, perm):
        return True

    def has_module_perms(self, module):
        return True

    def __str__(self):
        return self.get_full_name()

    @property
    def is_staff(self):
        return self.is_admin
