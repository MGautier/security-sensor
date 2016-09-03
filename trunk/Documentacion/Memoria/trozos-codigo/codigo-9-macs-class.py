class MacsTestCase(TestCase):

    def setUp(self):
        Macs.objects.create(MAC="00:00:00:00:00:00:00:00:00:00:00:00:08:00", TAG="Mac local")
