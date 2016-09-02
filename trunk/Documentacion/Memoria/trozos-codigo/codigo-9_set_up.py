class PacketEventsInformationTestCase(TestCase):

    # Atributos internos de la clase

    timestamp = timezone.now()
    timestamp_insertion = timezone.now()

    def setUp(self):
        ip_source = Ips.objects.create(Ip="127.0.0.2", Hostname="localhost", Tag="localhost")
        ip_dest = Ips.objects.create(Ip="127.0.0.3", Hostname="localhost", Tag="localhost")
        port_source = Ports.objects.create(Tag="ftp")
        port_dest = Ports.objects.create(Tag="ssh")
        mac_source = Macs.objects.create(
            MAC="00:00:00:00:00:00:00:00:00:00:00:00:08:00",
            TAG="Mac local1"
        )
        mac_dest = Macs.objects.create(
            MAC="00:00:00:00:00:00:00:00:00:00:00:00:08:00",
            TAG="Mac local2"
        )
        log_sources = LogSources.objects.create(
            Description="Firewall of gnu/linux kernel",
            Type="Iptables",
            Model="iptables v1.4.21",
            Active=1,
            Software_Class="Firewall",
            Path="iptables",
        )
        event = Events.objects.create(
            Timestamp=self.timestamp,
            Timestamp_Insertion=self.timestamp_insertion,
            ID_Source=log_sources,
            Comment="Iptables Events",
        )
        PacketEventsInformation.objects.create(
            ID_IP_Source=ip_source,
            ID_IP_Dest=ip_dest,
            ID_Source_Port=port_source,
            ID_Dest_Port=port_dest,
            Protocol="ICMP",
            ID_Source_MAC=mac_source,
            ID_Dest_MAC=mac_dest,
            RAW_Info="LOG RAW INFO",
            TAG="Connection ICMP",
            id=event
        )
