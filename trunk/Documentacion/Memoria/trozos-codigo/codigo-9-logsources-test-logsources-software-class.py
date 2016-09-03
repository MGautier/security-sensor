def test_logsources_software_class(self):
    """
    Comprobacion de que la clase de software de la fuente de seguridad coincide con su asociada
    Returns:

    """
    log_source = LogSources.objects.get(Software_Class="Firewall")
    self.assertEqual(log_source.get_software_class(), "Firewall")
