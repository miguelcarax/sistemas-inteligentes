import nodo

class Frontera:
    def __init__(self,):
        self.frontera = []

    def insertar(self, nodoArbol):
        flag = True
        sup = len(self.frontera) - 1
        inf = 0
        #print(nodoArbol.get_valor())
        if len(self.frontera) != 0:
            while flag:
                medio = int((sup + inf) / 2) + 1
                if sup<=inf or self.frontera[medio].get_valor() == nodoArbol.get_valor():
                    self.frontera.insert(medio, nodoArbol)
                    flag = False
                elif self.frontera[medio].get_valor() > nodoArbol.get_valor():
                    sup = medio - 1
                elif self.frontera[medio].get_valor() < nodoArbol.get_valor():
                    inf = medio + 1
        else:
            self.frontera.append(nodoArbol)

    def sacar_elemento(self):
        #Ordenacion de la frontera por valor (menor a mayor)
        #self.frontera = sorted(self.frontera, key=lambda k: k.get_valor())
        #Devuelve el elemento de menor valor de la frontera y lo elimina
        return self.frontera.pop(0)

    def esVacia(self):
        return not self.frontera

    def numFrontera(self):
        return len(self.frontera)

    def insercionOrdenada(nodo):
        flag = True
        sup = len(frontera) - 1
        inf = 0
        while not flag:
            medio = (sup + inf) / 2
            if frontera[medio] > nodo.get_valor():
                sup = medio - 1
            elif frontera[medio] < nodo.get_valor():
                inf = medio + 1
            elif frontera[medio] == nodo.get_valor():
                frontera.insert(medio, nodo)
                flag = False

    ##################################################
    def getLista(self):
        return self.frontera
