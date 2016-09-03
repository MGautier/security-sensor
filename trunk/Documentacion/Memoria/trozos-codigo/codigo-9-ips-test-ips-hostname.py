def test_ips_hostname(self):
    """
    Comprobacion de que coinciden las ips con su hostname
    Returns:

    """
    loopback_1 = Ips.objects.get(Ip="127.0.0.2")
    loopback_2 = Ips.objects.get(Ip="127.0.0.3")
    self.assertEqual(loopback_1.get_hostname(), "localhost")
    self.assertEqual(loopback_2.get_hostname(), "localhost")
