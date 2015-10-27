class Frontera:
    def __init__(self):
        self.frontera = []

    def insertar(self, nodoArbol):
        self.frontera.append(nodoArbol)

    def sacar_elemento(self):
        #Ordenacion de la frontera por valor (menor a mayor)
        self.frontera = sorted(self.frontera, key=lambda k: k['valor'])
        #Devuelve el elemento de menor valor de la frontera y lo elimina
        return self.frontera.pop(0)

    def esVacia(self):
        return not self.frontera
