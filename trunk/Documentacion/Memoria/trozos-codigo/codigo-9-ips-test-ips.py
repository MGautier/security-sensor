def test_ips(self):
    """
    Comprobacion de que las ips asignadas coinciden
    Returns:

    """
    loopback_1 = Ips.objects.get(Ip="127.0.0.2")
    loopback_2 = Ips.objects.get(Ip="127.0.0.3")
    self.assertEqual(loopback_1.get_ip(), "127.0.0.2")
    self.assertEqual(loopback_2.get_ip(), "127.0.0.3")
