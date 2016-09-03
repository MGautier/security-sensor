def test_macs_mac(self):
    """
    Comprobacion de que la direccion mac coincide con su asociada
    Returns:

    """
    macs = Macs.objects.get(MAC="00:00:00:00:00:00:00:00:00:00:00:00:08:00")
    self.assertEqual(macs.get_mac(), "00:00:00:00:00:00:00:00:00:00:00:00:08:00")
