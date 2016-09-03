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
