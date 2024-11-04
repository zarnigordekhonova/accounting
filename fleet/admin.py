from django.contrib import admin
from .models import Company, CustomUser, Department, UserStatus

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(UserStatus)
admin.site.register(CustomUser)