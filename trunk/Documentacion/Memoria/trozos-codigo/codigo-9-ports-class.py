class PortsTestCase(TestCase):

    def setUp(self):
        Ports.objects.create(Tag="ftp")
