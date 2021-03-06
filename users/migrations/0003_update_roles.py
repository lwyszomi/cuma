# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-19 20:56
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings

from users.models import RoleType


def update_roles(*args, **kwargs):
    RoleType.objects.all().delete()

    for role_type in settings.DEFAULT_ROLES:
        RoleType.objects.get_or_create(
            name=role_type
        )


def revert_update_roles(*args, **kwargs):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_default_roles'),
    ]

    operations = [
        migrations.RunPython(update_roles, revert_update_roles)
    ]
