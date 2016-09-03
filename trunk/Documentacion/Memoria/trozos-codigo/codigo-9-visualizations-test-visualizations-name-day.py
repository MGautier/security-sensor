def test_visualizations_name_day(self):
    """
    Comprobacion de que el nombre del dia procesado coincide con su asociado
    Returns:

    """
    visualizations = Visualizations.objects.get(Name_Day="Wednesday")
    self.assertEqual(visualizations.get_name_day(), "Wednesday")
