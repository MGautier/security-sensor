def test_visualizations_process_events(self):
    """
    Comprobacion de que el numero de eventos registrados para la fecha coincide con el asociado
    Returns:

    """
    visualizations = Visualizations.objects.get(Process_Events=5)
    self.assertEqual(visualizations.get_process_events(), 5)
