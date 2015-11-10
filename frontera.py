import nodo
import heapq

class Frontera:
    def __init__(self,):
        self.frontera = []
        heapq.heapify(self.frontera)

    def insertar(self, nodoArbol):
        heapq.heappush(self.frontera, nodoArbol)

    def sacar_elemento(self):
        return heapq.heappop(self.frontera)

    def esVacia(self):
        return not self.frontera
