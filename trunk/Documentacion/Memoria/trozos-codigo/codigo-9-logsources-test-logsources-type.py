def test_logsources_type(self):
    """
    Comprobacion de que el tipo de la fuente de seguridad coincide con su asociado
    Returns:

    """
    log_source = LogSources.objects.get(Type="Iptables")
    self.assertEqual(log_source.get_type(), "Iptables")
