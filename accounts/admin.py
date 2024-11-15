from django.contrib import admin
from . models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ['-date_joined']
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'role', 'is_active')
 
    


admin.site.register(User, CustomUserAdmin)