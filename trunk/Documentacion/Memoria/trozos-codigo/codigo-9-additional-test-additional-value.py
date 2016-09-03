def test_packetadditionalinfo_value(self):
    """
    Comprobacion de que el valor del paquete, correspondiente a la etiqueta, coincide con su asociado
    Returns:

    """
    pai = PacketAdditionalInfo.objects.get(Value="32731 DF")
    self.assertEqual(pai.get_value(), "32731 DF")
