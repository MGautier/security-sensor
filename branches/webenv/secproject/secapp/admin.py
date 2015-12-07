from django.contrib import admin
from .models import Ips, Events, Ports, LogSources, PacketAdditionalInfo, PacketEventsInformation, Macs, Tags

# Register your models here.

admin.site.register(Ips)
admin.site.register(Events)
admin.site.register(Ports)
admin.site.register(LogSources)
admin.site.register(PacketAdditionalInfo)
admin.site.register(PacketEventsInformation)
admin.site.register(Macs)
admin.site.register(Tags)
