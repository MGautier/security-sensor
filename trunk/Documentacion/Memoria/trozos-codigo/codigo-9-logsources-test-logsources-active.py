def test_logsources_active(self):
    """
    Comprobacion de que la fuente de seguridad se encuentra activa una vez instanciada
    Returns:

    """
    log_source = LogSources.objects.get(Active=1)
    self.assertEqual(log_source.get_active(), 1)
