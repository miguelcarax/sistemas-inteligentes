#!/usr/bin/python
#Este archivo usa el encoding: utf-8

"""
Estructura principal
----------------------------------------
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
import distancia

graph = graph.Graph()

# Captura de los datos de Ciudad Real
# (MinLong, MinLat, MaxLon, MaxLat)

#map = osmapi.OsmApi().Map(-3.93128, 38.98423 , -3.92806, 38.98795)
map = osmapi.OsmApi().Map(-3.9524, 38.9531, -3.8877, 39.0086)
dict_nodes = {}
list_ways = []

for map_dict in map:
    # Tipo vía AND sea 'highway' AND residencial, nacional, peatonal
    if map_dict['type'] == 'way' and 'highway' in map_dict['data']['tag'] and map_dict['data']['tag']['highway'] in ['trunk', 'residential', 'pedestrian']:
        list_ways.append(map_dict['data'])
    elif map_dict['type'] == 'node':
        dict_nodes[map_dict['data']['id']] = map_dict['data']



for way_dict in list_ways:
    list_nodes = way_dict['nd']
    for i, node in enumerate(list_nodes):
        if not graph.node_exist(node):
            if i == 0:
                node_aux = dict_nodes[node]
                node_dic = {'lat' : node_aux['lat'], 'lon' : node_aux['lon'], 'id' : node_aux['id'], 'edges' : []}
                graph.add_node(node_dic)
            else:
                node_aux = dict_nodes[node]
                node_dic = {'lat' : node_aux['lat'], 'lon' : node_aux['lon'], 'id' : node_aux['id'], 'edges': []}
                graph.add_node(node_dic)
                #Devuelve la distancia entre los dos nodos
                dist = distancia.dist(graph.get_nodes()[list_nodes[i]]['lon'], graph.get_nodes()[list_nodes[i]]['lat'], graph.get_nodes()[list_nodes[i-1]]['lon'], graph.get_nodes()[list_nodes[i-1]]['lat'])
                graph.add_edge(list_nodes[i], list_nodes[i-1], dist)
                graph.add_edge(list_nodes[i-1], list_nodes[i], dist)
        else:
            if i != 0:
                dist = distancia.dist(graph.get_nodes()[list_nodes[i]]['lon'], graph.get_nodes()[list_nodes[i]]['lat'], graph.get_nodes()[list_nodes[i-1]]['lon'], graph.get_nodes()[list_nodes[i-1]]['lat'])
                graph.add_edge(list_nodes[i], list_nodes[i-1], dist)
                graph.add_edge(list_nodes[i-1], list_nodes[i], dist)



    #Impresión de las aristas de los nodos.
    #for i, node in enumerate(list_nodes):
    #    print("[node]",node,"->", graph.get_nodes()[node]['edges'])

#print(len(graph.get_nodes()))
#print("Nodos adyacentes a 806368792: ")
print(graph.get_ady(828480065))
