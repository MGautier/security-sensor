def test_historic_timestamp(self):
    """
    Comprobacion de que el timestamp del historico coincide con su asociado
    Returns:

    """
    historic = Historic.objects.get(Timestamp=self.timestamp)
    self.assertEqual(historic.get_timestamp(), self.timestamp)
