from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'username', 'is_staff']
    readonly_fields = ['id']

admin.site.register(CustomUser, CustomUserAdmin)
