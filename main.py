#!/usr/bin/python
#Este archivo usa el encoding: utf-8

import espacioEstados
import estado
import problema
import frontera
import nodo
import distancia
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

ANCHURA = 'ANCHURA'
PROFUNDIDAD = 'PROFUNDIDAD'
COSTO = 'COSTOUNIFORME'


def CrearSolucion(n_actual):
    solucion = []
    while n_actual.get_padre() is not None:
        solucion.insert(0,n_actual.get_estado())
        print(n_actual.get_costo())
        n_actual = n_actual.get_padre()
    solucion.insert(0,n_actual.get_estado())
    return solucion

def CrearListaNodosArbol(problema, lista_sucesores,n_actual, prof_max, estrategia):
    nodos_arbol = []

    if estrategia == 'PROFUNDIDAD':
        if n_actual.get_profundidad() < prof_max:
            if n_actual.get_padre() is not None:
                for suc in lista_sucesores:
                    if n_actual.get_padre().get_estado() != suc[1]:
                        nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,1/(n_actual.get_profundidad()+1)))
            else:
                for suc in lista_sucesores:
                    nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,1/(n_actual.get_profundidad()+1)))

    elif estrategia == 'ANCHURA':
        if n_actual.get_padre() is not None:
            for suc in lista_sucesores:
                if n_actual.get_padre().get_estado() != suc[1]:
                    nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,n_actual.get_profundidad()+1))
        else:
            for suc in lista_sucesores:
                nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,n_actual.get_profundidad()+1))

    elif estrategia == 'COSTOUNIFORME':
        if n_actual.get_padre() is not None:
            for suc in lista_sucesores:
                if n_actual.get_padre().get_estado() != suc[1]:
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
##############################################################################
    p_act = 0
    it=0
##############################################################################
    while not solucion and not frontera_l.esVacia():
        n_actual = frontera_l.sacar_elemento()
        print(n_actual)
        it+=1
##########################################################################

        p_actN = n_actual.get_profundidad()
        """
        if p_act != p_actN:
            p_act = p_actN
            print(p_act)
            print(frontera_l.numFrontera())
        """

###############################################################################
        if problema.esObjetivo(n_actual.get_estado()) :
            solucion = True
        else:
            lista_sucesores = problema.get_espacioEstados().sucesor(n_actual.get_estado())
            lista_nodos = CrearListaNodosArbol(problema,lista_sucesores,n_actual,prof_max,estrategia)
            for item in lista_nodos:
                #print(item, item.get_estado().getLocalizacion()['id'])
                frontera_l.insertar(item)
        """
        if it % 50 == 0:
            lista = frontera_l.getLista()
            #print(lista)
            solucion =  True
        """

    if solucion :
        estados_solucion = CrearSolucion(n_actual)
        #print(frontera_l.sacar_elemento())
        #print(frontera_l.getLista())
    return estados_solucion

def Busqueda(problema,estrategia,max_prof, inc_prof):
    solucion = []
    prof_act = inc_prof
    it=0

    while not solucion and (prof_act <= max_prof):
        print(it)
        solucion = Busqueda_acotada(problema,estrategia,prof_act)
        prof_act += inc_prof
        it+=1
    return solucion


espacioEstados = espacioEstados.EspacioEstados(-3.9524, 38.9531, -3.8877, 39.0086)
estadoInicial = estado.Estado(espacioEstados.getNodeOsm(806369151),[814770792])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(828480073),[828479978, 833754743])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(804689213),[765309507, 806369170])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(765309500),[522198147, 812955433])
#estadoInicial = estado.Estado(803292594,[814770929, 2963385997, 522198144
problema_l = problema.Problema(estadoInicial, espacioEstados)
solucion = Busqueda(problema_l, COSTO, 55, 1)

for item in solucion:
    print (item)
