from django.db import models


class RoleType(models.Model):
    name = models.CharField(max_length=168)
