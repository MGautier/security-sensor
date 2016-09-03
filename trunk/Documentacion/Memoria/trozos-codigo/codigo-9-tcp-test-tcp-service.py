def test_tcp_service(self):
    """
    Comprobacion de que el servicio asociado al protocolo coincide
    Returns:

    """
    port = Ports.objects.get(Tag="ssh")
    tcp = Tcp.objects.get(id=port)
    self.assertEqual(tcp.get_service(), "ssh")
