from django.contrib import admin
from .models import Branches, CustomUser, UserRoles, Roles, PasswordReset
# Register your models here.

admin.site.register(Branches)
admin.site.register(CustomUser)
admin.site.register(UserRoles)
admin.site.register(Roles)
admin.site.register(PasswordReset)