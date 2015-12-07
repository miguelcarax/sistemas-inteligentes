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


def CrearListaNodosArbol(problema_l, lista_sucesores,n_actual, prof_max, estrategia, opc_heuristica, podar):
    nodos_arbol = []

    if estrategia == 'PROFUNDIDAD':
        if prof_max == 0 or n_actual.get_profundidad() < prof_max:
            for suc in lista_sucesores:
                n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo()+suc[2], suc[0], n_actual.get_profundidad()+1, 1/(n_actual.get_profundidad()+1))
                if podar:
                    if not poda(estrategia, n_nuevo):
                        nodos_arbol.append(n_nuevo)
                else:
                    nodos_arbol.append(n_nuevo)


    elif estrategia == 'ANCHURA':
        for suc in lista_sucesores:
            n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo()+suc[2], suc[0], n_actual.get_profundidad()+1, n_actual.get_profundidad()+1)
            if podar:
                if not poda(estrategia, n_nuevo):
                    nodos_arbol.append(n_nuevo)
            else:
                nodos_arbol.append(n_nuevo)

    elif estrategia == 'COSTOUNIFORME':
        for suc in lista_sucesores:
            n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, n_actual.get_costo() + suc[2])
            if podar:
                if not poda(estrategia, n_nuevo):
                    nodos_arbol.append(n_nuevo)
            else:
                nodos_arbol.append(n_nuevo)

    elif estrategia == 'A':
        for suc in lista_sucesores:
            if opc_heuristica == 1:
                n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, (n_actual.get_costo() + suc[2]) + problema_l.h1(suc[1]))
            else:
                n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, (n_actual.get_costo() + suc[2]) + problema_l.h3(suc[1]))
            if podar:
                if not poda(estrategia, n_nuevo):
                    nodos_arbol.append(n_nuevo)
            else:
                nodos_arbol.append(n_nuevo)

    elif estrategia == 'VORAZ':
        for suc in lista_sucesores:
            n_nuevo = nodo.Nodo(n_actual, suc[1], n_actual.get_costo() + suc[2], suc[0], n_actual.get_profundidad()+1, problema_l.h1(suc[1]))
            if podar:
                if not poda(estrategia, n_nuevo):
                    nodos_arbol.append(n_nuevo)
            else:
                nodos_arbol.append(n_nuevo)

    return nodos_arbol

def Busqueda_acotada(problema_l,estrategia,prof_max, opc_heuristica, podar):
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
            lista_nodos = CrearListaNodosArbol(problema_l, lista_sucesores,n_actual,prof_max,estrategia, opc_heuristica, podar)
            for item in lista_nodos:
                frontera_l.insertar(item)
    if solucion :
        estados_solucion = CrearSolucion(n_actual)

    return nodos, estados_solucion

def Busqueda(problema,estrategia,max_prof, inc_prof, opc_heuristica, podar):
    solucion = []
    prof_act = inc_prof

    while not solucion and (prof_act <= max_prof):
        nodos, solucion = Busqueda_acotada(problema,estrategia,prof_act, opc_heuristica, podar)
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

"""
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

construirGPX(espacioEstados, estrategia, nodos, tiempo_procesamiento, solucion)"""


def datos():
    lat_1,lat_2 = -91,-91
    lon_1,lon_2 = -181,-181
    lista_nodos = []
    while(lat_1<-90 or lat_1>90 or lat_2<-90 or lat_2>90 or lon_1<-180 or lon_1>180 or lon_2<-180 or lon_2>180 ):
        print('Introduzca las coordenadas\n')
        print('\nIntroduzca la latidud del primer punto:\n')
        lat_1 = float(input())
        print('Introduzca la longitud del primer punto:\n')
        lon_1 = float(input())
        print('Introduzca la latidud del segundo punto:\n')
        lat_2 = float(input())
        print('Introduzca la longitud del segundo punto:\n')
        lon_2 = float(input())
        if(lat_1<-90 or lat_1>90 or lat_2<-90 or lat_2>90 or lon_1<-180 or lon_1>180 or lon_2<-180 or lon_2>180):
            print('Error. Introduzca unos valores correctos')

    coordenadas = (lat_1,lon_1,lat_2,lon_2)

    print('\nIntroduzca el nodo de partida:')
    nodoInicial = int(input())
    n_nodos =0

    while(n_nodos < 1):
        print('¿Cuántos nodos desea visitar:?')
        n_nodos = int(input())
        if (n_nodos < 1):
            print('Introduzca un valor mayor que cero.')

    n=0

    while(n<n_nodos):
        print('Introduzca el siguiente nodo:')
        nodosel = int(input())
        lista_nodos.append(nodosel)
        n += 1

    return coordenadas, nodoInicial, lista_nodos

continuar = True
introducirdatos = True

while(continuar):
    profundidad_max, incremento_profunidad = 0, 0
    opc_heuristica = 0
    op_poda = -1
    podar = False
    opcion = -1
    if introducirdatos:
        coordenadas, nodoInicial, lista_nodos = datos()
        introducirdatos = False


    while (opcion < 1 or opcion > 7 ):
        print('\nMenú inicial. Elija una estrategia:\n')
        print('1 - Profundidad')
        print('2 - Anchura')
        print('3 - Costo Unifirme')
        print('4 - Voraz')
        print('5 - A')
        print('6 - Introducir coordenadas y datos')
        print('7 - Salir del programa\n')
        print('Introduzca la opción deseada: \n')
        opcion = int(input())
        if(opcion < 1 or opcion > 7):
            print('\nError.Elija una opcion correcta.')


    if opcion == 1:
        estrategia = PROFUNDIDAD
        opcion_profundidad = -1
        while(opcion_profundidad<1 or opcion_profundidad>3):
            print('\nElija el tipo de profundidad que desea:\n')
            print('1 - Simple')
            print('2 - Acotada')
            print('3 - Iterativa')
            opcion_profundidad = int(input())
            if(opcion_profundidad<1 or opcion_profundidad>3):
                print('\nError.Elija una opcion correcta.')

        if opcion_profundidad == 1:
            profundidad_max, incremento_profunidad = 0, 0

        elif opcion_profundidad == 2:
            profundidad_max = 0
            while(profundidad_max < 1):
                print('\nIntroduzca la profundidad maxima: \n')
                profundidad_max = int(input())
                if profundidad_max < 1:
                    print('\nError. Introduzca una profundidad mayor que cero.')

            incremento_profunidad = profundidad_max

        elif opcion_profundidad == 3:

            profundidad_max = 0
            incremento_profunidad = 0
            while(profundidad_max < 1 or incremento_profunidad < 1 or incremento_profunidad > profundidad_max):
                print('\nIntroduzca la profundidad maxima: \n')
                profundidad_max = int(input())
                print('\nIntroduzca el incremento de profundidad en cada iteración: \n')
                incremento_profunidad = int(input())
                if profundidad_max < 1:
                    print('\nError. Introduzca una profundidad mayor que cero.')
                if incremento_profunidad < 1 or incremento_profunidad > profundidad_max:
                    print('\nError. Introduzca un incremento mayor que cero y menor que la profundidad maxima.')

    elif opcion == 2:
        estrategia = ANCHURA

    elif opcion == 3:
        estrategia = COSTO

    elif opcion == 4:
        estrategia = VORAZ

    elif opcion == 5:
        estrategia = A
        opc_heuristica = -1
        while (opc_heuristica < 1 or opc_heuristica > 2):
            print('\nIntroduzca la heuristica que desea:\n')
            print('1 - Mayor distincia')
            print('2 - Mayor proyección')
            print('Elija la opción que desee:\n')
            opc_heuristica = int(input())
            if(opc_heuristica < 1 or opc_heuristica > 2):
                print('Error. Elija una opción correcta.')

    elif opcion == 6:
        coordenadas, nodoInicial, lista_nodos = datos()

    elif opcion == 7:
        continuar = False
        print('\nPrograma desarrollado por:\n')
        print('León Alcaide, Pablo')
        print('Ludeña Triviño, Marcos')
        print('Morecho Chacón, Miguel Ángel\n')
        print('Gracias por utilizar nuestro programa.\n\nFinalizando programa...\n')

    if opcion != 7:
        while(op_poda<1 or op_poda>2):
            print('\n¿Desea que el algoritmo realice poda?:\n')
            print('1 - Si')
            print('2 - No')
            print('Elija la opción que desee:\n')
            op_poda = int(input())
            if(op_poda<1 or op_poda>2):
                print('Error. Elija una opcion correcta.')

        if op_poda == 1:
            podar = True

        else:
            podar = False


        espacioEstados = espacioEstados.EspacioEstados(coordenadas)
        estadoInicial = estado.Estado(espacioEstados.getNodeOsm(nodoInicial),lista_nodos)
        
        try:
            problema_l = problema.Problema(estadoInicial, espacioEstados)
            resolver = True

        except problema.EstadoNoValido as e:
            print(e)
            resolver = False
            introducirdatos = True

        if resolver:
            t1 = time.clock()
            nodos, solucion = Busqueda(problema_l, estrategia, profundidad_max, incremento_profunidad, opc_heuristica, poda)
            t2 = time.clock()
            tiempo_procesamiento = t2-t1
            construirGPX(espacioEstados, estrategia, nodos, tiempo_procesamiento, solucion)

            print('\n¡Ruta construida!, Enhorabuena.\n')
