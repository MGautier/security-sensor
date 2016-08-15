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

    def test_packeteventsinformation_id_ip_source(self):
        """
        Comprobacion de que el objeto de ip origen (referencia al modelo relacional) coincide con su asociado
        Returns:

        """
        ip_source = Ips.objects.get(Ip="127.0.0.2")
        pei = PacketEventsInformation.objects.get(ID_IP_Source=ip_source)
        self.assertEqual(pei.get_id_ip_source(), ip_source)

    def test_packeteventsinformation_id_ip_dest(self):
        """
        Comprobacion de que el objeto de ip destino (referencia al modelo relacional) coincide con su asociado
        Returns:

        """
        ip_dest = Ips.objects.get(Ip="127.0.0.3")
        pei = PacketEventsInformation.objects.get(ID_IP_Dest=ip_dest)
        self.assertEqual(pei.get_id_ip_dest(), ip_dest)

    def test_packeteventsinformation_id_source_port(self):
        """
        Comprobacion de que el objeto de puerto origen (referencia al modelo relacional) coincide con su asociado
        Returns:

        """
        port_source = Ports.objects.get(Tag="ftp")
        pei = PacketEventsInformation.objects.get(ID_Source_Port=port_source)
        self.assertEqual(pei.get_id_source_port(), port_source)

    def test_packeteventsinformation_id_dest_port(self):
        """
        Comprobacion de que el objeto de puerto destino (referencia al modelo relacional) coincide con su asociado
        Returns:

        """
        port_dest = Ports.objects.get(Tag="ssh")
        pei = PacketEventsInformation.objects.get(ID_Dest_Port=port_dest)
        self.assertEqual(pei.get_id_dest_port(), port_dest)

    def test_packeteventsinformation_protocol(self):
        """
        Comprobacion de que el protocolo del paquete coincide con su asociado
        Returns:

        """
        pei = PacketEventsInformation.objects.get(Protocol="ICMP")
        self.assertEqual(pei.get_protocol(), "ICMP")

    def test_packeteventsinformation_id_source_mac(self):
        """
        Comprobacion de que el objeto de mac origen (referencia al modelo relacional) coincide con su asociado
        Returns:

        """
        mac_source = Macs.objects.get(TAG="Mac local1")
        pei = PacketEventsInformation.objects.get(ID_Source_MAC=mac_source)
        self.assertEqual(pei.get_id_source_mac(), mac_source)

    def test_packeteventsinformation_id_dest_mac(self):
        """
        Comprobacion de que el objeto de mac destino (referencia al modelo relacional) coincide con su asociado
        Returns:

        """
        mac_dest = Macs.objects.get(TAG="Mac local2")
        pei = PacketEventsInformation.objects.get(ID_Dest_MAC=mac_dest)
        self.assertEqual(pei.get_id_dest_mac(), mac_dest)

    def test_packeteventsinformation_raw_info(self):
        """
        Comprobacion de que el log en formato RAW coincide con su asociado
        Returns:

        """
        pei = PacketEventsInformation.objects.get(RAW_Info="LOG RAW INFO")
        self.assertEqual(pei.get_raw_info(), "LOG RAW INFO")

    def test_packeteventsinformation_tag(self):
        """
        Comprobacion de que la etiqueta especificada para el paquete coincide con su asociado
        Returns:

        """
        pei = PacketEventsInformation.objects.get(TAG="Connection ICMP")
        self.assertEqual(pei.get_tag(), "Connection ICMP")

    def test_packeteventsinformation_id(self):
        """
        Comprobacion de que el objeto de ip origen (referencia al modelo relacional) coincide con su asociado
        Returns:

        """
        event = Events.objects.get(Timestamp=self.timestamp)
        pei = PacketEventsInformation.objects.get(id=event)
        self.assertEqual(pei.get_id(), event)
