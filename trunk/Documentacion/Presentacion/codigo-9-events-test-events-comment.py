def test_events_comment(self):
    """
    Comprobacion de que el comentario asociado al evento pertenece al asociado
    Returns:

    """
    events = Events.objects.get(Comment="Iptables Events")
    self.assertEqual(events.get_comment(), "Iptables Events")
