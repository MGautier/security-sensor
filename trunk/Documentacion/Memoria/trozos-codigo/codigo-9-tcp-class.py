class TcpTestCase(TestCase):

    def setUp(self):
        port = Ports.objects.create(Tag="ssh")
        Tcp.objects.create(id=port, Service="ssh", Description="Conexion ssh")
