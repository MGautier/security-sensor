def test_tags_tag(self):
    """
    Comprobacion de que la etiqueta (keyword) coincide con su asociada
    Returns:

    """
    tags = Tags.objects.get(Tag="URGP")
    self.assertEqual(tags.get_tag(), "URGP")
