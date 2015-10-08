#!/usr/bin/python
#Este archivo usa el encoding: utf-8

"""
graph {
    nodo : { }
}

nodo {
    'lat'   : latitud
    'lon'   : longitud
    'tag'   : etiquetas(?) { }
    'id'    : id del nodo
    'edges' : [(nodo, coste), ...]
}
"""

import osmapi
import graph

graph = graph.Graph()
# Captura de los datos de Ciudad Real
map = osmapi.OsmApi().Map(-3.9524, 38.9531 , -3.8877, 39.0086)

for map_dict in map:
    # Selecionamos las vías
    if map_dict['type'] == 'way':
        way_dict = osmapi.OsmApi().WayGet(map_dict['data']['id'])
        list_nodes = way_dict['nd']

        for i, node in enumerate(list_nodes):
            if not graph.node_exist(node):
                if i == 0:
                    node_aux = osmapi.OsmApi().NodeGet(node)
                    node_dic = {'lat' : node_aux['lat'], 'lon' : node_aux['lon'], 'id' : node_aux['id'], 'edges' : []}
                    graph.add_node(node_dic)

                else:
                    node_aux = osmapi.OsmApi().NodeGet(node)
                    node_dic = {'lat' : node_aux['lat'], 'lon' : node_aux['lon'], 'id' : node_aux['id'], 'edges': []}
                    graph.add_node(node_dic)
                    graph.add_edge(list_nodes[i], list_nodes[i-1], 0)
                    graph.add_edge(list_nodes[i-1], list_nodes[i], 0)
                    break
