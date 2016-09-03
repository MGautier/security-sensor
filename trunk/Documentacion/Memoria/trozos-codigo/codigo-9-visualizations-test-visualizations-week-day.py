def test_visualizations_week_day(self):
    """
    Comprobacion de que el dia de la semana pertenece a la asociada
    Returns:

    """
    visualizations = Visualizations.objects.get(Week_Day=2)
    self.assertEqual(visualizations.get_week_day(), 2)
