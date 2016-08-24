# Author: Moises Gautier Gomez
# Proyecto fin de carrera - Ing. en Informatica
# Universidad de Granada

from django.test import TestCase
from .models import LogSources, Events, PacketEventsInformation, Macs,\
    PacketAdditionalInfo, Visualizations, Ips, Ports, Tcp, Udp, Tags, Historic
from django.utils import timezone
from datetime import date


class IpsTestCase(TestCase):
    def setUp(self):
        Ips.objects.create(Ip="127.0.0.2", Hostname="localhost", Tag="localhost")
        Ips.objects.create(Ip="127.0.0.3", Hostname="localhost", Tag="localhost")

    def test_ips(self):
        """
        Comprobacion de que las ips asignadas coinciden
        Returns:

        """
        loopback_1 = Ips.objects.get(Ip="127.0.0.2")
        loopback_2 = Ips.objects.get(Ip="127.0.0.3")
        self.assertEqual(loopback_1.get_ip(), "127.0.0.2")
        self.assertEqual(loopback_2.get_ip(), "127.0.0.3")

    def test_ips_hostname(self):
        """
        Comprobacion de que coinciden las ips con su hostname
        Returns:

        """
        loopback_1 = Ips.objects.get(Ip="127.0.0.2")
        loopback_2 = Ips.objects.get(Ip="127.0.0.3")
        self.assertEqual(loopback_1.get_hostname(), "localhost")
        self.assertEqual(loopback_2.get_hostname(), "localhost")

    def test_ips_tag(self):
        """
        Comprobacion de que los tags asociados a las ips coinciden
        Returns:

        """
        loopback_1 = Ips.objects.get(Ip="127.0.0.2")
        loopback_2 = Ips.objects.get(Ip="127.0.0.3")
        self.assertEqual(loopback_1.get_tag(), "localhost")
        self.assertEqual(loopback_2.get_tag(), "localhost")


class PortsTestCase(TestCase):

    def setUp(self):
        Ports.objects.create(Tag="ftp")

    def test_ports_tag(self):
        """
        Comprobacion de que el tag asociado al puerto coincide
        Returns:

        """
        port = Ports.objects.get(Tag="ftp")
        self.assertEqual(port.get_tag(), "ftp")


class TcpTestCase(TestCase):

    def setUp(self):
        port = Ports.objects.create(Tag="ssh")
        Tcp.objects.create(id=port, Service="ssh", Description="Conexion ssh")

    def test_tcp_service(self):
        """
        Comprobacion de que el servicio asociado al protocolo coincide
        Returns:

        """
        port = Ports.objects.get(Tag="ssh")
        tcp = Tcp.objects.get(id=port)
        self.assertEqual(tcp.get_service(), "ssh")

    def test_tcp_description(self):
        """
        Comprobacion de que la descripcion asociada al protocolo coincide
        Returns:

        """
        port = Ports.objects.get(Tag="ssh")
        tcp = Tcp.objects.get(id=port)
        self.assertEqual(tcp.get_description(), "Conexion ssh")

    def test_tcp_id(self):
        """
        Comprobacion de que el puerto (objeto heredado) coincide con el asociado al protocolo
        Returns:

        """
        port = Ports.objects.get(Tag="ssh")
        tcp = Tcp.objects.get(id=port)
        self.assertEqual(tcp.get_id(), port)


class UdpTestCase(TestCase):

    def setUp(self):
        port = Ports.objects.create(Tag="ssh")
        Udp.objects.create(id=port, Service="ssh", Description="Conexion ssh")

    def test_udp_service(self):
        """
        Comprobacion de que el servicio asociado al protocolo coincide
        Returns:

        """
        port = Ports.objects.get(Tag="ssh")
        udp = Udp.objects.get(id=port)
        self.assertEqual(udp.get_service(), "ssh")

    def test_udp_description(self):
        """
        Comprobacion de que la descripcion asociada al protocolo coincide
        Returns:

        """
        port = Ports.objects.get(Tag="ssh")
        udp = Udp.objects.get(id=port)
        self.assertEqual(udp.get_description(), "Conexion ssh")

    def test_udp_id(self):
        """
        Comprobacion de que el puerto (objeto heredado) coincide con el asociado al protocolo
        Returns:

        """
        port = Ports.objects.get(Tag="ssh")
        udp = Udp.objects.get(id=port)
        self.assertEqual(udp.get_id(), port)


class TagsTestCase(TestCase):

    def setUp(self):
        Tags.objects.create(Description="Urgent Pointer", Tag="URGP")

    def test_tags_description(self):
        """
        Comprobacion de que la descripcion de la etiqueta coincide con su asociada
        Returns:

        """
        tags = Tags.objects.get(Description="Urgent Pointer")
        self.assertEqual(tags.get_description(), "Urgent Pointer")

    def test_tags_tag(self):
        """
        Comprobacion de que la etiqueta (keyword) coincide con su asociada
        Returns:

        """
        tags = Tags.objects.get(Tag="URGP")
        self.assertEqual(tags.get_tag(), "URGP")


class MacsTestCase(TestCase):

    def setUp(self):
        Macs.objects.create(MAC="00:00:00:00:00:00:00:00:00:00:00:00:08:00", TAG="Mac local")

    def test_macs_mac(self):
        """
        Comprobacion de que la direccion mac coincide con su asociada
        Returns:

        """
        macs = Macs.objects.get(MAC="00:00:00:00:00:00:00:00:00:00:00:00:08:00")
        self.assertEqual(macs.get_mac(), "00:00:00:00:00:00:00:00:00:00:00:00:08:00")

    def test_macs_tag(self):
        """
        Comprobacion de que la etiqueta que identifica a la direccion mac coincide con su asociada
        Returns:

        """
        macs = Macs.objects.get(TAG="Mac local")
        self.assertEqual(macs.get_tag(), "Mac local")


class LogSourcesTestCase(TestCase):

    def setUp(self):
        LogSources.objects.create(
            Description="Firewall of gnu/linux kernel",
            Type="Iptables",
            Model="iptables v1.4.21",
            Active=1,
            Software_Class="Firewall",
            Path="iptables",
        )

    def test_logsources_description(self):
        """
        Comprobacion de que la descripcion de la fuente de seguridad coincide con su asociada
        Returns:

        """
        log_source = LogSources.objects.get(Description="Firewall of gnu/linux kernel")
        self.assertEqual(log_source.get_description(), "Firewall of gnu/linux kernel")

    def test_logsources_type(self):
        """
        Comprobacion de que el tipo de la fuente de seguridad coincide con su asociado
        Returns:

        """
        log_source = LogSources.objects.get(Type="Iptables")
        self.assertEqual(log_source.get_type(), "Iptables")

    def test_logsources_model(self):
        """
        Comprobacion de que el modelo de la fuente de seguridad coincide con su asociado
        Returns:

        """
        log_source = LogSources.objects.get(Model="iptables v1.4.21")
        self.assertEqual(log_source.get_model(), "iptables v1.4.21")

    def test_logsources_active(self):
        """
        Comprobacion de que la fuente de seguridad se encuentra activa una vez instanciada
        Returns:

        """
        log_source = LogSources.objects.get(Active=1)
        self.assertEqual(log_source.get_active(), 1)

    def test_logsources_software_class(self):
        """
        Comprobacion de que la clase de software de la fuente de seguridad coincide con su asociada
        Returns:

        """
        log_source = LogSources.objects.get(Software_Class="Firewall")
        self.assertEqual(log_source.get_software_class(), "Firewall")

    def test_logsources_path(self):
        """
        Comprobacion de que el comando o path de ejecucion de la fuente coincide con su asociado
        Returns:

        """
        log_source = LogSources.objects.get(Path="iptables")
        self.assertEqual(log_source.get_path(), "iptables")


class HistoricTestCase(TestCase):

    # Atributos internos de la clase

    timestamp = timezone.now()

    def setUp(self):
        log_sources = LogSources.objects.create(
            Description="Firewall of gnu/linux kernel",
            Type="Iptables",
            Model="iptables v1.4.21",
            Active=1,
            Software_Class="Firewall",
            Path="iptables",
        )
        Historic.objects.create(
            ID_Source=log_sources,
            Timestamp=self.timestamp,
            Events=1,
        )

    def test_historic_source(self):
        """
        Comprobacion de que la fuente de seguridad a la que pertenece es igual a la asociada
        Returns:

        """
        log_sources = LogSources.objects.get(Type="Iptables")
        historic = Historic.objects.get(ID_Source=log_sources)
        self.assertEqual(historic.get_source(), log_sources)

    def test_historic_timestamp(self):
        """
        Comprobacion de que el timestamp del historico coincide con su asociado
        Returns:

        """
        historic = Historic.objects.get(Timestamp=self.timestamp)
        self.assertEqual(historic.get_timestamp(), self.timestamp)

    def test_historic_events(self):
        """
        Comprobacion de que el numero de eventos del historico coincide con su asociado
        Returns:

        """
        historic = Historic.objects.get(Events=1)
        self.assertEqual(historic.get_events(), 1)


class EventsTestCase(TestCase):

    # Atributos internos de la clase

    timestamp = timezone.now()
    timestamp_insertion = timezone.now()

    def setUp(self):
        log_sources = LogSources.objects.create(
            Description="Firewall of gnu/linux kernel",
            Type="Iptables",
            Model="iptables v1.4.21",
            Active=1,
            Software_Class="Firewall",
            Path="iptables",
        )
        Events.objects.create(
            Timestamp=self.timestamp,
            Timestamp_Insertion=self.timestamp_insertion,
            ID_Source=log_sources,
            Comment="Iptables Events",
        )

    def test_events_timestamp(self):
        """
        Comprobacion de que el timestamp del evento corresponde al del asociado
        Returns:

        """
        events = Events.objects.get(Timestamp=self.timestamp)
        self.assertEqual(events.get_timestamp(), self.timestamp)

    def test_events_timestamp_insertion(self):
        """
        Comprobacion de que el timestamp de inserccion del evento corresponde con el asociado
        Returns:

        """
        events = Events.objects.get(Timestamp_Insertion=self.timestamp_insertion)
        self.assertEqual(events.get_timestamp_insertion(), self.timestamp_insertion)

    def test_events_source(self):
        """
        Comprobacion de que la fuente de seguridad, a la que pertenece, es igual a la asociada
        Returns:

        """
        log_sources = LogSources.objects.get(Type="Iptables")
        events = Events.objects.get(ID_Source=log_sources)
        self.assertEqual(events.get_source(), log_sources)

    def test_events_comment(self):
        """
        Comprobacion de que el comentario asociado al evento pertenece al asociado
        Returns:

        """
        events = Events.objects.get(Comment="Iptables Events")
        self.assertEqual(events.get_comment(), "Iptables Events")


class VisualizationsTestCase(TestCase):

    def setUp(self):
        log_sources = LogSources.objects.create(
            Description="Firewall of gnu/linux kernel",
            Type="Iptables",
            Model="iptables v1.4.21",
            Active=1,
            Software_Class="Firewall",
            Path="iptables",
        )
        Visualizations.objects.create(
            Week_Month=1,
            Week_Day=2,
            Name_Day="Wednesday",
            Date=date(2016, 8, 10),
            Hour=18,
            ID_Source=log_sources,
            Process_Events=5
        )

    def test_visualizations_week_month(self):
        """
        Comprobacion de que la semana del mes pertenece a la asociada
        Returns:

        """
        visualizations = Visualizations.objects.get(Week_Month=1)
        self.assertEqual(visualizations.get_week_month(), 1)

    def test_visualizations_week_day(self):
        """
        Comprobacion de que el dia de la semana pertenece a la asociada
        Returns:

        """
        visualizations = Visualizations.objects.get(Week_Day=2)
        self.assertEqual(visualizations.get_week_day(), 2)

    def test_visualizations_name_day(self):
        """
        Comprobacion de que el nombre del dia procesado coincide con su asociado
        Returns:

        """
        visualizations = Visualizations.objects.get(Name_Day="Wednesday")
        self.assertEqual(visualizations.get_name_day(), "Wednesday")

    def test_visualizations_date(self):
        """
        Comprobacion de que la fecha registrada en el sistema coincide con la asociada
        Returns:

        """
        visualizations = Visualizations.objects.get(Date=date(2016, 8, 10))
        self.assertEqual(visualizations.get_date(), date(2016, 8, 10))

    def test_visualizations_hour(self):
        """
        Comprobacion de que la hora registrada en el sistema para la fecha procesada, coincide con la asociada
        Returns:

        """
        visualizations = Visualizations.objects.get(Hour=18)
        self.assertEqual(visualizations.get_hour(), 18)

    def test_visualizations_source(self):
        """
        Comprobacion de que la fuente de seguridad a la que pertenece, es igual a la asociada
        Returns:

        """
        log_sources = LogSources.objects.get(Type="Iptables")
        visualizations = Visualizations.objects.get(ID_Source=log_sources)
        self.assertEqual(visualizations.get_source(), log_sources)

    def test_visualizations_process_events(self):
        """
        Comprobacion de que el numero de eventos registrados para la fecha coincide con el asociado
        Returns:

        """
        visualizations = Visualizations.objects.get(Process_Events=5)
        self.assertEqual(visualizations.get_process_events(), 5)


class PacketEventsInformationTestCase(TestCase):

    # Atributos internos de la clase

    timestamp = timezone.now()
    timestamp_insertion = timezone.now()

    def setUp(self):
        ip_source = Ips.objects.create(Ip="127.0.0.2", Hostname="localhost", Tag="localhost")
        ip_dest = Ips.objects.create(Ip="127.0.0.3", Hostname="localhost", Tag="localhost")
        port_source = Ports.objects.create(Tag="ftp")
        port_dest = Ports.objects.create(Tag="ssh")
        mac_source = Macs.objects.create(MAC="00:00:00:00:00:00:00:00:00:00:00:00:08:00", TAG="Mac local1")
        mac_dest = Macs.objects.create(MAC="00:00:00:00:00:00:00:00:00:00:00:00:08:00", TAG="Mac local2")
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


class PacketAdditionalInfoTestCase(TestCase):

    # Atributos internos de la clase
    timestamp = timezone.now()
    timestamp_insertion = timezone.now()

    def setUp(self):
        ip_source = Ips.objects.create(Ip="127.0.0.2", Hostname="localhost", Tag="localhost")
        ip_dest = Ips.objects.create(Ip="127.0.0.3", Hostname="localhost", Tag="localhost")
        port_source = Ports.objects.create(Tag="ftp")
        port_dest = Ports.objects.create(Tag="ssh")
        mac_source = Macs.objects.create(MAC="00:00:00:00:00:00:00:00:00:00:00:00:08:00", TAG="Mac local1")
        mac_dest = Macs.objects.create(MAC="00:00:00:00:00:00:00:00:00:00:00:00:08:00", TAG="Mac local2")
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
        packet = PacketEventsInformation.objects.create(
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
        tag = Tags.objects.create(Description="Packet ID", Tag="ID")
        PacketAdditionalInfo.objects.create(
            ID_Tag=tag,
            ID_Packet_Events=packet,
            Value="32731 DF"
        )

    def test_packetadditionalinfo_id_tag(self):
        """
        Comprobacion de que el objeto tag (referencia al modelo relacional) coincide con su asociado
        Returns:

        """
        tag = Tags.objects.get(Tag="ID")
        pai = PacketAdditionalInfo.objects.get(ID_Tag=tag)
        self.assertEqual(pai.get_id_tag(), tag)

    def test_packetadditionalinfo_id_packet_events(self):
        """
        Comprobacion de que el packet events information al que pertenece (referencia al modelo relacional) coincide
        con su asociado
        Returns:

        """
        event = Events.objects.get(Timestamp=self.timestamp)
        packet = PacketEventsInformation.objects.get(id=event)
        pai = PacketAdditionalInfo.objects.get(ID_Packet_Events=packet)
        self.assertEqual(pai.get_id_packet_events(), packet)

    def test_packetadditionalinfo_value(self):
        """
        Comprobacion de que el valor del paquete, correspondiente a la etiqueta, coincide con su asociado
        Returns:

        """
        pai = PacketAdditionalInfo.objects.get(Value="32731 DF")
        self.assertEqual(pai.get_value(), "32731 DF")
