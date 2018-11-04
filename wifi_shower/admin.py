from django.contrib import admin
from .models import Device


class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    list_display = ('id', 'mac_id', 'secret_key', 'created_date', 'sold_date', 'user')


admin.site.register(Device, DeviceAdmin)
