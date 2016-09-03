def test_packetadditionalinfo_id_packet_events(self):
    """
    Comprobacion de que el packet events information al que pertenece (referencia al modelo relacional) coincide con su asociado
    Returns:

    """
    event = Events.objects.get(Timestamp=self.timestamp)
    packet = PacketEventsInformation.objects.get(id=event)
    pai = PacketAdditionalInfo.objects.get(ID_Packet_Events=packet)
    self.assertEqual(pai.get_id_packet_events(), packet)
