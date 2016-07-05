# Clase que alberga la informacion relacionada con el paquete extraido
# mediante el log. La gran mayoria de los campos
# son identificadores o claves foraneas a otros
# objetos/instancias de la base de datos.

class PacketEventsInformation(models.Model):
    ID_IP_Source = models.ForeignKey(Ips, models.SET_NULL, blank=True,
                                     null=True,
                                     related_name="ip_source")
    ID_IP_Dest = models.ForeignKey(Ips, models.SET_NULL, blank=True,
                                   null=True,
                                   related_name="ip_dest")
    ID_Source_Port = models.ForeignKey(Ports, models.SET_NULL, blank=True,
                                       null=True,
                                       related_name="port_source")
    ID_Dest_Port = models.ForeignKey(Ports, models.SET_NULL, blank=True,
                                     null=True,
                                     related_name="port_dest")
    Protocol = models.CharField(max_length=20, default='-')
    ID_Source_MAC = models.ForeignKey(Macs, models.SET_NULL, blank=True,
                                      null=True,
                                      related_name="mac_source")
    ID_Dest_MAC = models.ForeignKey(Macs, models.SET_NULL, blank=True,
                                    null=True,
                                    related_name="mac_dest")
    RAW_Info = models.TextField(default='-')
    TAG = models.CharField(max_length=255, default='-')
    id = models.OneToOneField(Events, on_delete=models.CASCADE,
                              primary_key=True)

    def __str__(self):
        return '%s' % self.id
