def test_packeteventsinformation_id_ip_dest(self):
    """
    Comprobacion de que el objeto de ip destino (referencia al modelo relacional) coincide con su asociado
    Returns:

    """
    ip_dest = Ips.objects.get(Ip="127.0.0.3")
    pei = PacketEventsInformation.objects.get(ID_IP_Dest=ip_dest)
    self.assertEqual(pei.get_id_ip_dest(), ip_dest)
