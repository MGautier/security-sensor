def test_packeteventsinformation_id_source_port(self):
    """
    Comprobacion de que el objeto de puerto origen (referencia al modelo relacional) coincide con su asociado
    Returns:

    """
    port_source = Ports.objects.get(Tag="ftp")
    pei = PacketEventsInformation.objects.get(ID_Source_Port=port_source)
    self.assertEqual(pei.get_id_source_port(), port_source)
