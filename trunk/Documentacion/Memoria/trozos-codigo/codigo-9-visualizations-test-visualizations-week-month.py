def test_visualizations_week_month(self):
    """
    Comprobacion de que la semana del mes pertenece a la asociada
    Returns:

    """
    visualizations = Visualizations.objects.get(Week_Month=1)
    self.assertEqual(visualizations.get_week_month(), 1)
