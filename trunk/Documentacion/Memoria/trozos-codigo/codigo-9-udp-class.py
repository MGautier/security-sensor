class UdpTestCase(TestCase):

    def setUp(self):
        port = Ports.objects.create(Tag="ssh")
        Udp.objects.create(id=port, Service="ssh", Description="Conexion ssh")
