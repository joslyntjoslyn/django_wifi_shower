from django.contrib import admin
from .models import Device, Profile


class DeviceAdmin(admin.ModelAdmin):
    fields = ('mac_id', 'secret_key', 'created_date', 'sold_date', 'user')
    readonly_fields = ('created_date',)
    list_display = ('id', 'mac_id', 'secret_key', 'created_date', 'sold_date', 'user')


class ProfileAdmin(admin.ModelAdmin):
    fields = ('name', 'user', 'preheat_cycle', 'shower_cycle', 'shower_temp', 'old_shower_habits', 'water_used',
              'water_saved', 'challenge_level', 'created_date', 'last_shower_date')
    readonly_fields = ('preheat_cycle', 'shower_cycle', 'shower_temp', 'old_shower_habits', 'water_used',
              'water_saved', 'challenge_level', 'created_date', 'last_shower_date')
    list_display = ('id', 'name', 'user', 'preheat_cycle', 'shower_cycle', 'shower_temp', 'old_shower_habits', 'water_used',
                    'water_saved', 'challenge_level', 'created_date', 'last_shower_date')


admin.site.register(Device, DeviceAdmin)
admin.site.register(Profile, ProfileAdmin)
