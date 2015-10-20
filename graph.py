
#!/bin/python3
"""
Clase grafo que hace de interfaz para tratar con el grafo de nodos.
"""

class Graph:
    def __init__(self):
        self.nodes = {}

    def get_nodes(self):
        return self.nodes

    def get_node(self, node_id):
        return self.nodes['node_id']

    def get_ady(self, node_id):
        return self.nodes[node_id]['edges']

    def add_node(self, node):
        self.nodes[node['id']] = node #MODIFICADO

    def add_edge(self, node_src, node_end, cost):
        #Se encarga de añadir una tupla (nodo, coste) a la lista de adayacencia de un nodo
        self.nodes[node_src]['edges'].append((node_end, cost))

    def node_exist(self, node_id):
        return node_id in self.nodes
