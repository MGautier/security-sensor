def test_packetadditionalinfo_id_tag(self):
    """
    Comprobacion de que el objeto tag (referencia al modelo relacional) coincide con su asociado
    Returns:

    """
    tag = Tags.objects.get(Tag="ID")
    pai = PacketAdditionalInfo.objects.get(ID_Tag=tag)
    self.assertEqual(pai.get_id_tag(), tag)
