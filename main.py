#!/usr/bin/python
#Este archivo usa el encoding: utf-8

import espacioEstados
import estado
import problema
import frontera
import nodo
import distancia
import os
import time
import datetime

"""
La altitud de todos los puntos va a ser 0.
Crear sello de tiempo para cada nodo basado en los metros de nodo a nodo.

Se añaden etiquetas: estrategia utilizada, costo de la solucion, profundidad de la solucion
encontrada, informacion de complejidad temporal y espacial, estado inicial.

visualizer GPX ---> visualizer GPS


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
#CONSTANTES

COSTO       = 'COSTOUNIFORME'
ANCHURA     = 'ANCHURA'
PROFUNDIDAD = 'PROFUNDIDAD'
A           = 'A'
VORAZ       = 'VORAZ'

estados = {}


def CrearSolucion(n_actual):
    """
    Devuelve la lista de estados solucion al problema. Va cogiendo sucesivamente los padres a los nodos solución el arbol hasta que llega a la raíz.
    """
    solucion = []
    while n_actual.get_padre() is not None:
        solucion.insert(0,n_actual)
        n_actual = n_actual.get_padre()

    solucion.insert(0,n_actual)
    return solucion


def poda(estrategia, nodo):
    podaF = True
    est_codificado = nodo.get_estado().codificar()
    if estrategia == PROFUNDIDAD:
        if est_codificado not in estados or estados[est_codificado] > nodo.get_costo():
            estados[est_codificado] = nodo.get_costo()
            podaF = False
    else:
        if est_codificado not in estados or estados[est_codificado] > nodo.get_valor():
            estados[est_codificado] = nodo.get_valor()
            podaF = False
    return podaF


def CrearListaNodosArbol(problema_l, lista_sucesores,n_actual, prof_max, estrategia):
    nodos_arbol = []

    if estrategia == 'PROFUNDIDAD':
        if prof_max == 0 or n_actual.get_profundidad() < prof_max:
            for suc in lista_sucesores:
                n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo()+suc[2], suc[0], n_actual.get_profundidad()+1, 1/(n_actual.get_profundidad()+1))
                if not poda(estrategia, n_nuevo):
                    nodos_arbol.append(n_nuevo)


    elif estrategia == 'ANCHURA':
        for suc in lista_sucesores:
            n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo()+suc[2], suc[0], n_actual.get_profundidad()+1, n_actual.get_profundidad()+1)
            if not poda(estrategia, n_nuevo):
                nodos_arbol.append(n_nuevo)

    elif estrategia == 'COSTOUNIFORME':
        for suc in lista_sucesores:
            n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, n_actual.get_costo() + suc[2])
            if not poda(estrategia, n_nuevo):
                nodos_arbol.append(n_nuevo)

    elif estrategia == 'A':
        for suc in lista_sucesores:
            n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, (n_actual.get_costo() + suc[2]) + problema_l.h1(suc[1]))
            if not poda(estrategia, n_nuevo):
                nodos_arbol.append(n_nuevo)

    elif estrategia == 'VORAZ':
        for suc in lista_sucesores:
            n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, problema_l.h1(suc[1]))
            if not poda(estrategia, n_nuevo):
                nodos_arbol.append(n_nuevo)

    return nodos_arbol

def Busqueda_acotada(problema_l,estrategia,prof_max):
    nodos = 0
    frontera_l = frontera.Frontera()
    solucion = False
    estados_solucion = []
    n_inicial = nodo.Nodo(None, problema_l.get_estadoInicial(),0,None,0,0)
    frontera_l.insertar(n_inicial)

    while not solucion and not frontera_l.esVacia():
        n_actual = frontera_l.sacar_elemento()
        nodos += 1
        if problema_l.esObjetivo(n_actual.get_estado()):
            solucion = True
        else:
            lista_sucesores = problema_l.get_espacioEstados().sucesor(n_actual.get_estado())
            lista_nodos = CrearListaNodosArbol(problema_l, lista_sucesores,n_actual,prof_max,estrategia)
            for item in lista_nodos:
                frontera_l.insertar(item)
    if solucion :
        estados_solucion = CrearSolucion(n_actual)

    return nodos, estados_solucion

def Busqueda(problema,estrategia,max_prof, inc_prof):
    solucion = []
    prof_act = inc_prof

    while not solucion and (prof_act <= max_prof):
        nodos, solucion = Busqueda_acotada(problema,estrategia,prof_act)
        prof_act += inc_prof

    return nodos, solucion

def construirGPX(espacioEstados, estrategia, complejidad_espacial, complejidad_temporal, solucion):
    profundidad_solucion = solucion[len(solucion)-1].get_profundidad()
    costo_solucion = solucion[len(solucion)-1].get_costo()
    estadoInicial = solucion[0].get_estado()
    ts = time.time()
    velocidad = 1 #1 m/s
    it=0
    with open('{0}.gpx'.format(estrategia),'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>')
        file.write('\n<gpx\n  version="1.0"\n  creator="Miguel Angel, Pablo y Marcos">')
        file.write('\n<metadata>\
                    \n\t<estrategia>{0}</estrategia>\
                    \n\t<costo>{1}</costo>\
                    \n\t<profundidad>{2}</profundidad>\
                    \n\t<complejidad_temporal>{3}</complejidad_temporal>\
                    \n\t<complejidad_espacial>{4}</complejidad_espacial>\
                \n</metadata>'
                    .format(estrategia, costo_solucion, profundidad_solucion, complejidad_temporal, complejidad_espacial))
        file.write('\n<wpt lat="{0}" lon="{1}">\
                    \n\t<name>{2}</name>\
                    \n</wpt>'\
                    .format(estadoInicial.getLocalizacion()['lat'], estadoInicial.getLocalizacion()['lon'], estadoInicial.getLocalizacion()['id']))
        for item in estadoInicial.getLista():
            file.write('\n<wpt lat="{0}" lon="{1}">\
                        \n\t<name>{2}</name>\
                        \n</wpt>'\
                        .format(espacioEstados.getNodeOsm(item)['lat'], espacioEstados.getNodeOsm(item)['lon'], item))

        file.write('\n<trk>\n\t<name>Ruta</name>\n\t\t<trkseg>')
        while it < len(solucion):
            item = solucion[it]
            if it!=0 :
                ts += ((item.get_costo() - solucion[it-1].get_costo()) / velocidad)
            file.write('\n\t\t\t<trkpt lat="{0}" lon="{1}">\
                        \n\t\t\t\t<ele>0</ele>\
                        \n\t\t\t\t<time>{2}</time>\
                        \n\t\t\t\t<name>{3}</name>\
                        \n\t\t\t\t<costo>{4}</costo>\
                        \n\t\t\t\t<valor>{5}</valor>\
                        \n\t\t\t\t<profundidad>{6}</profundidad>\
                        \n\t\t\t</trkpt>'\
                        .format(item.get_estado().getLocalizacion()['lat'], item.get_estado().getLocalizacion()['lon'],
                                datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), item.get_estado().getLocalizacion()['id'], item.get_costo(), item.get_valor(), item.get_profundidad()))
            it += 1
        file.write('\n\t\t</trkseg>\
                    \n\t</trk>\
                    \n</gpx>')


# main
estrategia  = COSTO
nodoInicial = 812954564
#lista       = [803292583, 812954600]
coordenadas = (-3.9524, 38.9531, -3.8877, 39.0086)
#coordenadas = (-3.9426, 38.9978, -3.9101, 38.9685)

espacioEstados = espacioEstados.EspacioEstados(coordenadas)
estadoInicial = estado.Estado(espacioEstados.getNodeOsm(835519284),[801797283,794373412,818781546, 824372789, 804689127])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(835519284),[801797283,794373412])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(nodoInicial),lista)
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(804689213),[765309507, 806369170])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(765309500),[522198147, 812955433])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(803292594),[814770929, 2963385997, 522198144])
problema_l = problema.Problema(estadoInicial, espacioEstados)
# Búsqueda(problema, estrategia, Profunidad Máxima, Incremento Profundidad)
profundidad_max, incremento_profunidad = 0, 0
t1 = time.clock()
nodos, solucion = Busqueda(problema_l, estrategia, profundidad_max, incremento_profunidad)
t2 = time.clock()
tiempo_procesamiento = t2-t1

construirGPX(espacioEstados, estrategia, nodos, tiempo_procesamiento, solucion)

# Escritura en el archivo de la solución al problema
