def test_events_timestamp_insertion(self):
    """
    Comprobacion de que el timestamp de inserccion del evento corresponde con el asociado
    Returns:

    """
    events = Events.objects.get(Timestamp_Insertion=self.timestamp_insertion)
    self.assertEqual(events.get_timestamp_insertion(), self.timestamp_insertion)
