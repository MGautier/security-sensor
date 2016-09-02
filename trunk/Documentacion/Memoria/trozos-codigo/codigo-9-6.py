def test_packeteventsinformation_id_source_mac(self):
    """
    Comprobacion de que el objeto de mac origen (referencia al modelo relacional) coincide con su asociado
    Returns:

    """
    mac_source = Macs.objects.get(TAG="Mac local1")
    pei = PacketEventsInformation.objects.get(ID_Source_MAC=mac_source)
    self.assertEqual(pei.get_id_source_mac(), mac_source)
