import osmapi
import graph
import distancia
import estado
"""
localizacion = diccionario tipo nodo
lista        = lista de id de nodos
"""
class EspacioEstados:

    def __init__(self, coor):
        #Construimos el grafo físico en el que estará basado nuestro espacio de estados
        self.graph = graph.Graph()
        self.CrearGrafoFisico(graph, coor[0], coor[1], coor[2], coor[3])

    def CrearGrafoFisico(self, graph, MinLong, MinLat, MaxLon, MaxLat):
        map = osmapi.OsmApi().Map(MinLong, MinLat, MaxLon, MaxLat)
        print("leido")
        dict_nodes = {}
        list_ways = []
        """
         A continución lo que llevamos a cabo es que vamos accediendo a cada uno de los diccionarios (nodos o vías) de la lista de diccionarios inicial.
         En caso de que el elemento sea una vía (type=way), que su atributo 'highway' sea del tipo 'residencial', 'peatonal' y 'nacional'.
         Si se cumplen estas condiciones este elemento es añadido a una lista de calles para ser tratadas, para ir sacando los nodos de esa calle.
         En caso de que sea un nodo, lo añadimos a la lista de nodos para ser añadidos al grafo.
         En las calles hacemos lo mismo que con los nodos, solo que en dos pasos, primero tratamos la calle para sacar sus nodos y después añadimos esos nodos al grafo, en caso de que no estén añadidos ya.
         """
        for map_dict in map:
            # Tipo vía AND sea 'highway' AND residencial, nacional, peatonal
            if map_dict['type'] == 'way' and 'highway' in map_dict['data']['tag'] and map_dict['data']['tag']['highway'] in ['trunk', 'residential', 'pedestrian']:
                list_ways.append(map_dict['data'])
            elif map_dict['type'] == 'node':
                dict_nodes[map_dict['data']['id']] = map_dict['data']

        """
        Como al sacar los nodos de las calles estás solo tienen como información su id y nosotros necesitamos más información, lo que hacemos es ir cogiendo los nodos de las calles y buscandolos en el diccionario de nodos totales que tenemos, que es auxiliar.
        Después sacamos la información que necesitamos de ese nodo de 'dict_nodes' y creamos el nodo auxiliar para después añadirlo al grafo.
        ·list_ways  : lista de calles que hemos recopilado antes.
        ·way_dict   : objeto iterador en la lista de calles.
        ·list_nodes : la lista de nodos que tiene una calle.
        La sintaxis es la siguiente:
        ·Si el nodo no existe en el grafo y este no es el primero lo añadimos al grafo, en caso de que no sea el primero, lo añadimos igualmente y después creamos el 'arco' entre el y el anterior y viceversa (el elemento actual de la lista 'i' y el elemento anterior 'i-1').
        ·Todo esto se realiza mediante la interfaz del grafo 'graph.add_node()' y 'graph.add_edge()'.
        ·Para crear los arcos de los nodos que coinciden en varias calles lo hacemos mediante la comprobación de que dicho nodo ya está en el grafo, ya que la otra calle en la que está ya la hemos recorrido.
        """
        for way_dict in list_ways:
            list_nodes = way_dict['nd']
            for i, node in enumerate(list_nodes):
                if not self.graph.node_exist(node):
                    if i == 0:
                        node_aux = dict_nodes[node]
                        node_dic = {'lat' : node_aux['lat'], 'lon' : node_aux['lon'], 'id' : node_aux['id'], 'edges' : []}
                        self.graph.add_node(node_dic)
                    else:
                        node_aux = dict_nodes[node]
                        node_dic = {'lat' : node_aux['lat'], 'lon' : node_aux['lon'], 'id' : node_aux['id'], 'edges': []}
                        self.graph.add_node(node_dic)
                        #Devuelve la distancia entre los dos nodos
                        dist = distancia.dist(self.graph.get_nodes()[list_nodes[i]]['lon'], self.graph.get_nodes()[list_nodes[i]]['lat'], self.graph.get_nodes()[list_nodes[i-1]]['lon'], self.graph.get_nodes()[list_nodes[i-1]]['lat'])
                        self.graph.add_edge(list_nodes[i], list_nodes[i-1], dist)
                        self.graph.add_edge(list_nodes[i-1], list_nodes[i], dist)
                else:
                    if i != 0:
                        dist = distancia.dist(self.graph.get_nodes()[list_nodes[i]]['lon'], self.graph.get_nodes()[list_nodes[i]]['lat'], self.graph.get_nodes()[list_nodes[i-1]]['lon'], self.graph.get_nodes()[list_nodes[i-1]]['lat'])
                        self.graph.add_edge(list_nodes[i], list_nodes[i-1], dist)
                        self.graph.add_edge(list_nodes[i-1], list_nodes[i], dist)

    #Comprueba si el estado existe en el grafo y todos los nodos que le quedan por visitar
    #también existen en el grafo
    def esValido(self, estado):
        flag = self.graph.node_exist(estado.getLocalizacion()['id'])
        if flag:
            for elemento in estado.getLista():
                flag = self.graph.node_exist(elemento)
                if not flag:
                    break

        return flag

    def sucesor(self, estado_l):
        #adyacencia = [(nodo, coste), (nodo, coste), ...]
        adyacencia = self.graph.get_ady(estado_l.getLocalizacion()['id'])
        sucesores  = []
        for item in adyacencia:
            #miramos si el item está en la lista de los que quedan por recorrer
            #sucesor = (nombre_accion, objeto_estado, coste)
            if item[0] in estado_l.getLista():
                estado_l.getLista().remove(item[0])
                sucesores.append(("Desde {0} hasta {1}.".format(estado_l.getLocalizacion()['id'], item[0]), estado.Estado(self.graph.get_node(item[0]), estado_l.getLista()), item[1]))
                estado_l.getLista().append(item[0])
            else:
                sucesores.append(("Desde {0} hasta {1}.".format(estado_l.getLocalizacion()['id'], item[0]), estado.Estado(self.graph.get_node(item[0]), estado_l.getLista()), item[1]))

        return sucesores

    def getNodeOsm(self,id):
        return self.graph.get_node(id)
