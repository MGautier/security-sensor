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
