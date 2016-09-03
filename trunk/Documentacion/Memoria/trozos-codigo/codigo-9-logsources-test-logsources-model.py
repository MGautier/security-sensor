def test_logsources_model(self):
    """
    Comprobacion de que el modelo de la fuente de seguridad coincide con su asociado
    Returns:

    """
    log_source = LogSources.objects.get(Model="iptables v1.4.21")
    self.assertEqual(log_source.get_model(), "iptables v1.4.21")
