from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Device, Profile, User
from .forms import CustomUserChangeForm, CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    list_display = ('email', 'is_active', 'date_joined')
    search_fields = ('email',)
    ordering = ('email',)


class DeviceAdmin(admin.ModelAdmin):
    fields = ('mac_id', 'secret_key', 'created_date', 'sold_date', 'user')
    readonly_fields = ('created_date', 'secret_key')
    list_display = ('mac_id', 'secret_key', 'created_date', 'sold_date', 'user')


class ProfileAdmin(admin.ModelAdmin):
    fields = ('name', 'user', 'preheat_cycle', 'shower_cycle', 'shower_temp', 'old_shower_habits', 'water_used',
              'water_saved', 'challenge_level', 'created_date', 'last_shower_date')
    readonly_fields = ('preheat_cycle', 'shower_cycle', 'shower_temp', 'old_shower_habits', 'water_used',
                       'water_saved', 'challenge_level', 'created_date', 'last_shower_date')
    list_display = ('user', 'name', 'preheat_cycle', 'shower_cycle', 'shower_temp', 'old_shower_habits', 'water_used',
                    'water_saved', 'challenge_level', 'created_date', 'last_shower_date')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Profile, ProfileAdmin)
