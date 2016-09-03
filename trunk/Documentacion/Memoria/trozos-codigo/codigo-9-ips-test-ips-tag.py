def test_ips_tag(self):
    """
    Comprobacion de que los tags asociados a las ips coinciden
    Returns:

    """
    loopback_1 = Ips.objects.get(Ip="127.0.0.2")
    loopback_2 = Ips.objects.get(Ip="127.0.0.3")
    self.assertEqual(loopback_1.get_tag(), "localhost")
    self.assertEqual(loopback_2.get_tag(), "localhost")
