class IpsTestCase(TestCase):
    def setUp(self):
        Ips.objects.create(Ip="127.0.0.2", Hostname="localhost", Tag="localhost")
        Ips.objects.create(Ip="127.0.0.3", Hostname="localhost", Tag="localhost")
