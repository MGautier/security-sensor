def test_packeteventsinformation_raw_info(self):
    """
    Comprobacion de que el log en formato RAW coincide con su asociado
    Returns:

    """
    pei = PacketEventsInformation.objects.get(RAW_Info="LOG RAW INFO")
    self.assertEqual(pei.get_raw_info(), "LOG RAW INFO")
