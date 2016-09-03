def test_udp_service(self):
    """
    Comprobacion de que el servicio asociado al protocolo coincide
    Returns:

    """
    port = Ports.objects.get(Tag="ssh")
    udp = Udp.objects.get(id=port)
    self.assertEqual(udp.get_service(), "ssh")
