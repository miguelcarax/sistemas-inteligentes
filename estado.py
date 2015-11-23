class Estado:

    def __init__(self, localizacion={}, lista=[]):
        self.localizacion = localizacion
        self.lista = sorted(lista)

    def getLista(self):
        return self.lista

    def getLocalizacion(self):
        return self.localizacion

    def codificar(self):
        cadena = str(self.localizacion['id'])
        for item in self.lista:
            cadena += "-" + str(item)
        return cadena

    def codificarLista(self):
        cadena = ''
        for item in self.lista:
            cadena += str(item) + '-'
        return cadena

    def __repr__(self):
        informacion = '[NODO {0}][por visitar: {1}]'.format(self.localizacion['id'], self.lista)
        return informacion

    def __eq__(self, other):
        """ Decide si los dos elementos son iguales"""
        return other.localizacion == self.localizacion and other.lista == self.lista
