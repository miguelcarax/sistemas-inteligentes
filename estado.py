class Estado:

    def __init__(self, localizacion={}, lista=[]):
        self.localizacion = localizacion
        self.lista = lista

    def getLista(self):
        return self.lista

    def getLocalizacion(self):
        return self.localizacion

    def __repr__(self):
        #return str(self.localizacion['id']) + "por visitar: "+ str(self.lista)
        informacion = '[NODO {0}][por visitar: {1}]'.format(self.localizacion['id'], self.lista)
        return informacion