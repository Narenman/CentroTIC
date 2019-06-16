from django.contrib import admin
from .models import DeviceDescriptor, DeviceOwner, \
    RulsetInfo, FrequencyRange, Geolocation, DeviceValidity, Spectrum, \
        Departamento, Frequency, EventTime, SpectrumSchedule, SpectrumSpec
# Register your models here.
admin.site.register(DeviceDescriptor)
admin.site.register(DeviceOwner)
admin.site.register(RulsetInfo)
admin.site.register(FrequencyRange)
admin.site.register(Geolocation)
admin.site.register(DeviceValidity)
admin.site.register(Spectrum)
admin.site.register(Departamento)
admin.site.register(Frequency)
admin.site.register(EventTime)
admin.site.register(SpectrumSchedule)
admin.site.register(SpectrumSpec)

