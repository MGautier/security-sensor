def test_packeteventsinformation_id_ip_source(self):
    """
    Comprobacion de que el objeto de ip origen (referencia al modelo relacional) coincide con su asociado
    Returns:

    """
    ip_source = Ips.objects.get(Ip="127.0.0.2")
    pei = PacketEventsInformation.objects.get(ID_IP_Source=ip_source)
    self.assertEqual(pei.get_id_ip_source(), ip_source)
