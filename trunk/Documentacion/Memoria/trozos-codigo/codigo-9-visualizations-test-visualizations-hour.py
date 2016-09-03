def test_visualizations_hour(self):
    """
    Comprobacion de que la hora registrada en el sistema para la fecha procesada, coincide con la asociada
    Returns:

    """
    visualizations = Visualizations.objects.get(Hour=18)
    self.assertEqual(visualizations.get_hour(), 18)
