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
