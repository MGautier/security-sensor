def test_packeteventsinformation_id_dest_port(self):
    """
    Comprobacion de que el objeto de puerto destino (referencia al modelo relacional) coincide con su asociado
    Returns:

    """
    port_dest = Ports.objects.get(Tag="ssh")
    pei = PacketEventsInformation.objects.get(ID_Dest_Port=port_dest)
    self.assertEqual(pei.get_id_dest_port(), port_dest)
