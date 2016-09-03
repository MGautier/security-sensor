def test_historic_events(self):
    """
    Comprobacion de que el numero de eventos del historico coincide con su asociado
    Returns:

    """
    historic = Historic.objects.get(Events=1)
    self.assertEqual(historic.get_events(), 1)
