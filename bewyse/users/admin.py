from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')