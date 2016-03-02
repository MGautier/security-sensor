from django.contrib import admin
from .models import Ips, LogSources, Events, Ports, Tags, Macs, PacketAdditionalInfo, PacketEventsInformation, Tcp, Udp
from .models import Visualizations

# Register your models here.

admin.site.register(Ips)
admin.site.register(LogSources)
admin.site.register(Events)
admin.site.register(Ports)
admin.site.register(Tags)
admin.site.register(Macs)
admin.site.register(PacketAdditionalInfo)
admin.site.register(PacketEventsInformation)
admin.site.register(Tcp)
admin.site.register(Udp)
admin.site.register(Visualizations)
