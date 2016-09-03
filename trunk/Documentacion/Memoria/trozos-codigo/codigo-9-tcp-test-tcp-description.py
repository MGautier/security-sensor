def test_tcp_description(self):
    """
    Comprobacion de que la descripcion asociada al protocolo coincide
    Returns:

    """
    port = Ports.objects.get(Tag="ssh")
    tcp = Tcp.objects.get(id=port)
    self.assertEqual(tcp.get_description(), "Conexion ssh")
