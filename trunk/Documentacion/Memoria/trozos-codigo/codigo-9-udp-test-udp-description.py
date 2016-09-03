def test_udp_description(self):
    """
    Comprobacion de que la descripcion asociada al protocolo coincide
    Returns:

    """
    port = Ports.objects.get(Tag="ssh")
    udp = Udp.objects.get(id=port)
    self.assertEqual(udp.get_description(), "Conexion ssh")
