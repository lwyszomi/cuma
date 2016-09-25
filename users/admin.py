from django.contrib import admin
from users.models import RoleType


class RoleTypeAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)

admin.site.register(RoleType, RoleTypeAdmin)
