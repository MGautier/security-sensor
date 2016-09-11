def test_events_timestamp(self):
    """
    Comprobacion de que el timestamp del evento corresponde al del asociado
    Returns:

    """
    events = Events.objects.get(Timestamp=self.timestamp)
    self.assertEqual(events.get_timestamp(), self.timestamp)
