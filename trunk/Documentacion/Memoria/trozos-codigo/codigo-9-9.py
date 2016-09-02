def test_packeteventsinformation_tag(self):
    """
    Comprobacion de que la etiqueta especificada para el paquete coincide con su asociado
    Returns:

    """
    pei = PacketEventsInformation.objects.get(TAG="Connection ICMP")
    self.assertEqual(pei.get_tag(), "Connection ICMP")
