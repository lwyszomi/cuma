from django.contrib import admin
from users.models import RoleType


class ToleTypeAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)

admin.site.register(RoleType, ToleTypeAdmin)
