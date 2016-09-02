def test_packeteventsinformation_id(self):
    """
    Comprobacion de que el objeto de ip origen (referencia al modelo relacional) coincide con su asociado
    Returns:

    """
    event = Events.objects.get(Timestamp=self.timestamp)
    pei = PacketEventsInformation.objects.get(id=event)
    self.assertEqual(pei.get_id(), event)
