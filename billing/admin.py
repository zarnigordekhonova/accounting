from django.contrib import admin
from .models import (Facility, FacilityHistory, Broker, BrokerHistory, LoadProcess,
                     Status, Load, LoadHistory, LoadFile, LoadStop)
# Register your models here.
admin.site.register(Facility)
admin.site.register(FacilityHistory)
admin.site.register(Broker)
admin.site.register(BrokerHistory)
admin.site.register(LoadProcess)
admin.site.register(Status)
admin.site.register(Load)
admin.site.register(LoadHistory)
admin.site.register(LoadFile)
admin.site.register(LoadStop)
