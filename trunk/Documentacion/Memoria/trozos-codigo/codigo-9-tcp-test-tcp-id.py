def test_tcp_id(self):
    """
    Comprobacion de que el puerto (objeto heredado) coincide con el asociado al Protocolos
    Returns:

    """
    port = Ports.objects.get(Tag="ssh")
    tcp = Tcp.objects.get(id=port)
    self.assertEqual(tcp.get_id(), port)
