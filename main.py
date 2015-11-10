#!/usr/bin/python
#Este archivo usa el encoding: utf-8

import espacioEstados
import estado
import problema
import frontera
import nodo
import distancia
import os

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
#CONSTANTES

COSTO       = 'COSTOUNIFORME'
ANCHURA     = 'ANCHURA'
PROFUNDIDAD = 'PROFUNDIDAD'


def CrearSolucion(n_actual):
    """
    Devuelve la lista de estados solucion al problema. Va cogiendo sucesivamente los padres a los nodos solución el arbol hasta que llega a la raíz.
    """
    solucion = []
    while n_actual.get_padre() is not None:
        solucion.insert(0,n_actual.get_estado())
        n_actual = n_actual.get_padre()
    solucion.insert(0,n_actual.get_estado())
    return solucion

def EsAntecesor(n_actual, e_suc):
    """ Método utilizado para evitar estados repetidos en un mismo camino. Mira en los predecesores si ese mismo estado existe"""
    flag = True
    while n_actual.get_padre() is not None and flag:
        if n_actual.get_estado() == e_suc:
            flag = False
        n_actual = n_actual.get_padre()

    if n_actual.get_estado() == e_suc:
        flag = False

    return flag

def CrearListaNodosArbol(problema, lista_sucesores,n_actual, prof_max, estrategia):
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
        if n_actual.get_padre() is not None:
            for suc in lista_sucesores:
                if EsAntecesor(n_actual, suc[1]):
                    nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,n_actual.get_profundidad()+1))
        else:
            for suc in lista_sucesores:
                nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,n_actual.get_profundidad()+1))

    elif estrategia == 'COSTOUNIFORME':
        if n_actual.get_padre() is not None:
            for suc in lista_sucesores:
                if EsAntecesor(n_actual, suc[1]):
                    nodos_arbol.append(nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, n_actual.get_costo() + suc[2]))
        else:
            for suc in lista_sucesores:
                nodos_arbol.append(nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, n_actual.get_costo() + suc[2]))

    return nodos_arbol

def Busqueda_acotada(problema,estrategia,prof_max):
    frontera_l = frontera.Frontera()
    n_inicial = nodo.Nodo(None, problema.get_estadoInicial(),0,None,0,0)
    frontera_l.insertar(n_inicial)
    solucion = False
    estados_solucion = []

    while not solucion and not frontera_l.esVacia():
        n_actual = frontera_l.sacar_elemento()
        p_actN = n_actual.get_profundidad()

        if problema.esObjetivo(n_actual.get_estado()) :
            solucion = True
        else:
            lista_sucesores = problema.get_espacioEstados().sucesor(n_actual.get_estado())
            lista_nodos = CrearListaNodosArbol(problema,lista_sucesores,n_actual,prof_max,estrategia)
            for item in lista_nodos:
                frontera_l.insertar(item)

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
estrategia  = PROFUNDIDAD
nodoInicial = 828480073
coordenadas = (-3.9524, 38.9531, -3.8877, 39.0086)

espacioEstados = espacioEstados.EspacioEstados(coordenadas)
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(806369151),[814770792])
estadoInicial = estado.Estado(espacioEstados.getNodeOsm(nodoInicial),[828479978, 833754743])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(804689213),[765309507, 806369170])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(765309500),[522198147, 812955433])
#estadoInicial = estado.Estado(803292594,[814770929, 2963385997, 522198144
problema_l = problema.Problema(estadoInicial, espacioEstados)
# Búsqueda(problema, estrategia, Profunidad Máxima, Incremento Profundidad)
profundidad_max, incremento_profunidad = 55, 1
solucion = Busqueda(problema_l, estrategia, profundidad_max, incremento_profunidad)

# Escritura en el archivo de la solución al problema
with open('solucion.out','w') as file:
    file.write('Coordenadas de búsqueda: {0}\nNodo inicial: {1}\n'.format(coordenadas, nodoInicial))
    file.write('Algoritmo de búsqueda: {0}\n\n'.format(estrategia))
    for index, item in enumerate(solucion):
        file.write('[{0}]{1}\n'.format(index, item))
