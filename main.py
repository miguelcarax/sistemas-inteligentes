#!/usr/bin/python
#Este archivo usa el encoding: utf-8

import espacioEstados
import estado
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

    # Impresión de las aristas de los nodos.
    #    for i, node in enumerate(list_nodes):
    #        print("[node]",node,"->", graph.get_nodes()[node]['edges'])

espacioEstados = espacioEstados.EspacioEstados(-3.9524, 38.9531, -3.8877, 39.0086)
estadoInicial = estado.Estado(espacioEstados.getGraph().get_node(828480065),[828480058, 12345, 54321])
#lista = estados.sucesor(estado)
for item in espacioEstados.sucesor(estadoInicial):
    print('[SUCESOR]',item)
"""
for item in lista:
    localizacion = item[1].getLocalizacion()['id']
    nodos = item[1].getLista()
    print(str(item[0]) + " " + str(localizacion) + " " + str(nodos) + " " + str(item[2]))
    print("\n")
"""
