def test_ports_tag(self):
    """
    Comprobacion de que el tag asociado al puerto coincide
    Returns:

    """
    port = Ports.objects.get(Tag="ftp")
    self.assertEqual(port.get_tag(), "ftp")
