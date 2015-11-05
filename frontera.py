import nodo
import heapq

class Frontera:
    def __init__(self,):
        self.frontera = []
        heapq.heapify(self.frontera)
    def insertar(self, nodoArbol):
        #self.frontera.append(nodoArbol)
        heapq.heappush(self.frontera, nodoArbol)
        """
        flag = True
        sup = len(self.frontera) - 1
        inf = 0
        print(nodoArbol.get_valor())
        if len(self.frontera) > 2:
            while flag:
                medio = int((sup + inf) / 2)
                if sup - inf <= 1 or self.frontera[medio].get_valor() == nodoArbol.get_valor():
                    if sup == inf and self.frontera[medio].get_valor() > nodoArbol.get_valor():
                        self.frontera.insert(medio, nodoArbol)
                    else:
                        self.frontera.insert(medio+1, nodoArbol)
                    flag = False
                elif self.frontera[medio].get_valor() > nodoArbol.get_valor():
                    sup = medio
                elif self.frontera[medio].get_valor() < nodoArbol.get_valor():
                    inf = medio
        elif len(self.frontera) == 2:
            if self.frontera[0].get_valor() < nodoArbol.get_valor():
                self.frontera.insert(0, nodoArbol)
            elif self.frontera[1].get_valor() < nodoArbol.get_valor():
                self.frontera.insert(1, nodoArbol)
            else:
                self.frontera.insert(2, nodoArbol)
        else:
            self.frontera.append(nodoArbol)
        """

    def sacar_elemento(self):
        #Ordenacion de la frontera por valor (menor a mayor)
        #self.frontera = sorted(self.frontera, key=lambda k: k.get_valor())
        #Devuelve el elemento de menor valor de la frontera y lo elimina
        #return self.frontera.pop(0)
        return heapq.heappop(self.frontera)

    def esVacia(self):
        return not self.frontera

    def numFrontera(self):
        return len(self.frontera)

    ##################################################
    def getLista(self):
        return self.frontera
