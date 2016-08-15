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
