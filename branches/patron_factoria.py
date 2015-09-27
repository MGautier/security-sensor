

class Source():

    def start(self):
        print "Iniciando fuente"
        self.procesar()

    def procesar(self):
        pass

    def tipo(self):
        pass



class Firewall (Source):
    def tipo(self):
        print "Soy un Firewall"

    def procesar (self):
        print "Procesando log de Firewall"


class IDS (Source):
    def tipo(self):
        print "Soy una IDS"

    def procesar (self):
        print "Procesando log de IDS"

#tipo_fuente = raw_input ("Que fuente vamos a crear?: ")
listaFuentes = ["Firewall", "IDS"]

for tipoFuente in listaFuentes:

    fuente = locals()[tipoFuente]()
    fuente.tipo()
    fuente.start()






