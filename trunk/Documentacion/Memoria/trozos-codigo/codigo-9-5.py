def test_packeteventsinformation_protocol(self):
    """
    Comprobacion de que el protocolo del paquete coincide con su asociado
    Returns:

    """
    pei = PacketEventsInformation.objects.get(Protocol="ICMP")
    self.assertEqual(pei.get_protocol(), "ICMP")
