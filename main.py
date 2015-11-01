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

def CrearSolucion(n_actual):
    solucion = []
    while n_actual.get_padre() is not None:
        solucion.insert(0,n_actual.get_estado())
        n_actual = n_actual.get_padre()
    solucion.insert(0,n_actual.get_estado())
    return solucion

def CrearListaNodosArbol(problema, lista_sucesores,n_actual, prof_max, estrategia):
    nodos_arbol = []

    if estrategia == 'PROFUNDIDAD':
        if prof_max > n_actual.get_profundidad():
            for suc in lista_sucesores:
                nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,1/(n_actual.get_profundidad()+1)))

    elif estrategia == 'ANCHURA':
        for suc in lista_sucesores:
            nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,n_actual.get_profundidad()+1))

    elif estrategia == 'COSTO UNIFORME':
        for suc in lista_sucesores:
            nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,n_actual.get_costo()+suc[2]))

    elif estrategia == 'A':
        flag = False
        n_visitar = n_actual.get_estado().getLista()

        locAct = n_actual.get_estado().getLocalizacion()
        lonAct = locAct['lon']
        latAct = locAct['lat']

        for item in n_visitar:
            if not flag:
                locCerc = problema.get_espacioEstados().getNodeOsm(item)
                loncerc = locCerc['lon']
                latcerc = locCerc['lat']
                flag = True
            else:
                locItem = problema.get_espacioEstados().getNodeOsm(item)
                lonItem = locItem['lon']
                latItem = locItem['lat']
                if distancia.dist(lonAct,latAct,loncerc,latcerc) > distancia.dist(lonAct,latAct,lonItem,latItem):
                    locCerc = problema.get_espacioEstados().getNodeOsm(item)
                    loncerc = locCerc['lon']
                    latcerc = locCerc['lat']

        for suc in lista_sucesores:
            nodos_arbol.append(nodo.Nodo(n_actual,suc[1],n_actual.get_costo()+suc[2],suc[0],n_actual.get_profundidad()+1,n_actual.get_costo()+suc[2]+distancia.dist(lonAct,latAct,loncerc,latcerc)))


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
##########################################################################
        """
        p_actN = n_actual.get_profundidad()
        it+=1
        if p_act != p_actN:
            p_act = p_actN
            print(p_act)
            print(frontera_l.numFrontera())
        """

###############################################################################
        if problema.esObjetivo(n_actual.get_estado()) :
            solucion = True
        else :
            lista_sucesores = problema.get_espacioEstados().sucesor(n_actual.get_estado())
            lista_nodos = CrearListaNodosArbol(problema,lista_sucesores,n_actual,prof_max,estrategia)
            for item in lista_nodos:
                frontera_l.insertar(item)

        #if it % 15000 == 0:
            #lista = frontera_l.getLista()
            #print(lista)
            #solucion =  True
        #    print(n_actual.get_valor())
    if solucion :
        estados_solucion = CrearSolucion(n_actual)
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

    # Impresión de las aristas de los nodos.
    #    for i, node in enumerate(list_nodes):
    #        print("[node]",node,"->", graph.get_nodes()[node]['edges'])

espacioEstados = espacioEstados.EspacioEstados(-3.9524, 38.9531, -3.8877, 39.0086)
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(828480073),[833754743])
#estadoInicial = estado.Estado(espacioEstados.getNodeOsm(828480073),[828479978, 833754743])
estadoInicial = estado.Estado(espacioEstados.getNodeOsm(804689213),[765309507, 806369170])
estadoInicial = estado.Estado(espacioEstados.getNodeOsm(765309500),[522198147, 812955433])
#estadoInicial = estado.Estado(803292594,[814770929, 2963385997, 522198144])
problema_l = problema.Problema(estadoInicial, espacioEstados)

solucion = Busqueda(problema_l, 'ANCHURA', 55, 1)

for item in solucion:
    print (item)
