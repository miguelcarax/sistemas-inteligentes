
#!/bin/python3
"""
Clase grafo que hace de interfaz para tratar con los datos de los grafos.
"""

class Graph:
    #Constructor
    def __init__(self):
        self.nodes = {}

    #Devuelve los nodos del grafo (diccionario)
    def get_nodes(self):
        return self.nodes

    #Devuelve los nodos adyacentes de un nodo
    def get_ady(self, node_id):
        return self.nodes[node_id]['edges']

    #Añade un nodo al grafo
    def add_node(self, node):
        self.nodes[node['id']] = node #MODIFICADO

    #Se encarga de añadir una tupla (nodo, coste) a la lista de adayacencia de un nodo
    def add_edge(self, node_src, node_end, cost):
        self.nodes[node_src]['edges'].append((node_end, cost))

    #Devuelve si un nodo dado existe dentro del grafo
    def node_exist(self, node_id):
        return node_id in self.nodes

    def get_node(self, id):
        return self.nodes[id]
