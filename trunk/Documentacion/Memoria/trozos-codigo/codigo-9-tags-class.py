class TagsTestCase(TestCase):

    def setUp(self):
        Tags.objects.create(Description="Urgent Pointer", Tag="URGP")
