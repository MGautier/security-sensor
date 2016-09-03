def test_visualizations_source(self):
    """
    Comprobacion de que la fuente de seguridad a la que pertenece, es igual a la asociada
    Returns:

    """
    log_sources = LogSources.objects.get(Type="Iptables")
    visualizations = Visualizations.objects.get(ID_Source=log_sources)
    self.assertEqual(visualizations.get_source(), log_sources)
