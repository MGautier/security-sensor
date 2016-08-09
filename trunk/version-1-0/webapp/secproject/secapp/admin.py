from django.contrib import admin
from .models import Ips, LogSources, Events, Ports, Tags, Macs, PacketAdditionalInfo, PacketEventsInformation, Tcp, Udp
from .models import Visualizations, Historic

# Aqui se registran los modelos de interaccion de la base de datos con los que vamos a trabajar en la aplicacion.

# Author: Moises Gautier Gomez
# Proyecto fin de carrera - Ing. en Informatica
# Universidad de Granada

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
admin.site.register(Historic)
