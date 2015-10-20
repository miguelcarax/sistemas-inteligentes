import graph

class Estado:
    def __init__(self, localizacion={}, lista=[]):
        self.localizacion = localizacion
        self.lista = lista

    def getLista(self):
        return self.lista

    def Suc(self, estado):
