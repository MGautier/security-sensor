def test_macs_tag(self):
    """
    Comprobacion de que la etiqueta que identifica a la direccion mac coincide con su asociada
    Returns:

    """
    macs = Macs.objects.get(TAG="Mac local")
    self.assertEqual(macs.get_tag(), "Mac local")
