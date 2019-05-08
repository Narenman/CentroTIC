from django.contrib import admin
from .models import DeviceDescriptor, DeviceOwner, \
    RulsetInfo, FrequencyRange, Geolocation, DeviceValidity, Spectrum
# Register your models here.
admin.site.register(DeviceDescriptor)
admin.site.register(DeviceOwner)
admin.site.register(RulsetInfo)
admin.site.register(FrequencyRange)
admin.site.register(Geolocation)
admin.site.register(DeviceValidity)
admin.site.register(Spectrum)



