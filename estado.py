import graph
"""
localizacion = diccionario tipo nodo
lista        = lista de id de nodos
"""
class Estado:
    def __init__(self, localizacion={}, lista=[]):
        self.localizacion = localizacion
        self.lista = lista

    def getLista(self):
        return self.lista

    def sucesor(self):
        #adyacencia = [(nodo, coste), (nodo, coste), ...]
        adyacencia = graph.get_ady(self.localizacion['id'])
        sucesores  = []
        for item in adyacencia:
            #miramos si el item está en la lista de los que quedan por recorrer
            #sucesor = (nombre_accion, objeto_estado, coste)
            if item[0] in self.lista:
                self.lista.remove(item[0])
                sucesores.append("Desde{0}hasta{1}.".format(self.localizacion['id'], item[0]), (Estado(graph.get_node(item[0])), self.lista), item[1])
                self.lista.append(item[0])
            else:
                sucesores.append(Estado(graph.get_node(item[0]), self.lista)

        return sucesores

    def esValido(self):
        pass
