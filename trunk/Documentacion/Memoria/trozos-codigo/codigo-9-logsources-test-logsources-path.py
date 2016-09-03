def test_logsources_path(self):
    """
    Comprobacion de que el comando o path de ejecucion de la fuente coincide con su asociado
    Returns:

    """
    log_source = LogSources.objects.get(Path="iptables")
    self.assertEqual(log_source.get_path(), "iptables")
