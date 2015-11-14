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

estados = {}


def CrearSolucion(n_actual):
    """
    Devuelve la lista de estados solucion al problema. Va cogiendo sucesivamente los padres a los nodos solución el arbol hasta que llega a la raíz.
    """
    solucion = []
    print(n_actual.get_costo())
    while n_actual.get_padre() is not None:
        solucion.insert(0,n_actual.get_estado())
        n_actual = n_actual.get_padre()
    solucion.insert(0,n_actual.get_estado())
    return solucion

def EsAntecesor(n_actual, e_suc):
    """
     Método utilizado para evitar estados repetidos en un mismo camino. Mira en los predecesores si ese mismo estado existe
    """
    flag = True
    while n_actual.get_padre() is not None and flag:
        if n_actual.get_estado() == e_suc:
            flag = False
        n_actual = n_actual.get_padre()

    if n_actual.get_estado() == e_suc:
        flag = False

    return flag

def poda(nodo):
    podaF = True
    est_codificado = nodo.get_estado().codificar()
    if est_codificado not in estados or estados[est_codificado] > nodo.get_valor():
        estados[est_codificado] = nodo.get_valor()
        podaF = False
    return podaF


def CrearListaNodosArbol(problema_l, lista_sucesores,n_actual, prof_max, estrategia):
    nodos_arbol = []

    if estrategia == 'PROFUNDIDAD':
        if prof_max == 0 or n_actual.get_profundidad() < prof_max:
            if n_actual.get_padre() is not None:
                for suc in lista_sucesores:
                    if EsAntecesor(n_actual, suc[1]):
                        nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,1/(n_actual.get_profundidad()+1)))
            else:
                for suc in lista_sucesores:
                    nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,1/(n_actual.get_profundidad()+1)))

    elif estrategia == 'ANCHURA':
        for suc in lista_sucesores:
            n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo()+suc[2], suc[0], n_actual.get_profundidad()+1, n_actual.get_profundidad()+1)
            if not poda(n_nuevo):
                nodos_arbol.append(n_nuevo)

    elif estrategia == 'COSTOUNIFORME':
        for suc in lista_sucesores:
            n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, n_actual.get_costo() + suc[2])
            if not poda(n_nuevo):
                nodos_arbol.append(n_nuevo)

    elif estrategia == 'A':
        for suc in lista_sucesores:
            n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, (n_actual.get_costo() + suc[2]) + problema_l.h2(suc[1]))
            if not poda(n_nuevo):
                nodos_arbol.append(n_nuevo)


    return nodos_arbol

def Busqueda_acotada(problema_l,estrategia,prof_max):
    frontera_l = frontera.Frontera()
    n_inicial = nodo.Nodo(None, problema_l.get_estadoInicial(),0,None,0,0)
    frontera_l.insertar(n_inicial)
    solucion = False
    estados_solucion = []
    it = 0

    while not solucion and not frontera_l.esVacia():
        n_actual = frontera_l.sacar_elemento()

        ############################################
        """
        if(it%500 == 0):
            print(str(len(estados)) +" "+ str(len(frontera_l.frontera)) + " " + str(it))
        """
        ############################################
        it+=1
        if problema_l.esObjetivo(n_actual.get_estado()):
            solucion = True
        else:
            lista_sucesores = problema_l.get_espacioEstados().sucesor(n_actual.get_estado())
            lista_nodos = CrearListaNodosArbol(problema_l, lista_sucesores,n_actual,prof_max,estrategia)
            for item in lista_nodos:
                frontera_l.insertar(item)
    print(it)
    if solucion :
        estados_solucion = CrearSolucion(n_actual)

    return estados_solucion

def Busqueda(problema,estrategia,max_prof, inc_prof):
    solucion = []
    prof_act = inc_prof

    while not solucion and (prof_act <= max_prof):
        solucion = Busqueda_acotada(problema,estrategia,prof_act)
        prof_act += inc_prof

    return solucion

# main
estrategia  = COSTO
nodoInicial = 812954564
lista = [803292583, 812954600]
coordenadas = (-3.9524, 38.9531, -3.8877, 39.0086)

espacioEstados = espacioEstados.EspacioEstados(coordenadas)
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(835519284),[801797283,794373412,818781546, 824372789, 804689127, 828480073, 827212563, 804689127])
estadoInicial = estado.Estado(espacioEstados.getNodeOsm(835519284),[801797283,794373412])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(nodoInicial),lista)
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(804689213),[765309507, 806369170])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(765309500),[522198147, 812955433])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(803292594),[814770929, 2963385997, 522198144])
problema_l = problema.Problema(estadoInicial, espacioEstados)
# Búsqueda(problema, estrategia, Profunidad Máxima, Incremento Profundidad)
profundidad_max, incremento_profunidad = 50, 1
t1 = time.clock()
solucion = Busqueda(problema_l, estrategia, profundidad_max, incremento_profunidad)
t2 = time.clock()
print(t2-t1)

# Escritura en el archivo de la solución al problema
with open('solucion.out','w') as file:
    file.write('Coordenadas de búsqueda: {0}\nEstado Inicial: ({1}, {2})\n'.format(coordenadas, nodoInicial, lista))
    file.write('Algoritmo de búsqueda: {0}\n\n'.format(estrategia))
    for index, item in enumerate(solucion):
        file.write('[{0}]{1}\n'.format(index, item))
