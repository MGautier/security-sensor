def test_logsources_description(self):
    """
    Comprobacion de que la descripcion de la fuente de seguridad coincide con su asociada
    Returns:

    """
    log_source = LogSources.objects.get(Description="Firewall of gnu/linux kernel")
    self.assertEqual(log_source.get_description(), "Firewall of gnu/linux kernel")
