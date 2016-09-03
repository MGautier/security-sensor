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
