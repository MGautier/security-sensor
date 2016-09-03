def test_visualizations_date(self):
    """
    Comprobacion de que la fecha registrada en el sistema coincide con la asociada
    Returns:

    """
    visualizations = Visualizations.objects.get(Date=date(2016, 8, 10))
    self.assertEqual(visualizations.get_date(), date(2016, 8, 10))
