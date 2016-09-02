def test_packeteventsinformation_id_dest_mac(self):
    """
    Comprobacion de que el objeto de mac destino (referencia al modelo relacional) coincide con su asociado
    Returns:

    """
    mac_dest = Macs.objects.get(TAG="Mac local2")
    pei = PacketEventsInformation.objects.get(ID_Dest_MAC=mac_dest)
    self.assertEqual(pei.get_id_dest_mac(), mac_dest)
