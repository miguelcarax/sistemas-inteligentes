import espacioEstados
import estado
import distancia
import itertools


class EstadoNoValido(Exception):
    def __str__(self):
        return '¡¡¡Estado No Válido!!!\nIntroduzca uno válido.\n'

class Problema:

    def __init__(self, estadoInicial_l, espacioEstados_l):
        self.espacioEstados = espacioEstados_l
        if self.espacioEstados.esValido(estadoInicial_l):
            self.estadoInicial = estadoInicial_l
        else:
            raise EstadoNoValido

    def esObjetivo(self, estado_l):
        return not estado_l.lista

    def h1(self, estado):
        lonAct = self.espacioEstados.getNodeOsm(estado.localizacion)['lon']
        latAct = self.espacioEstados.getNodeOsm(estado.localizacion)['lat']
        lista = estado.lista
        distanciaMax = -1
        for item in lista:
            nodoDestino = self.espacioEstados.getNodeOsm(item)
            distanciaAux = distancia.dist(lonAct, latAct, nodoDestino['lon'], nodoDestino['lat'])
            if distanciaAux > distanciaMax:
                distanciaMax = distanciaAux

        return distanciaMax

    def h2(self, estado):
        maxlat = self.espacioEstados.getNodeOsm(estado.localizacion)['lat']
        minlat = maxlat
        maxlon = self.espacioEstados.getNodeOsm(estado.localizacion)['lon']
        minlon = maxlon
        lista = estado.lista
        for item in lista:
            nodo = self.espacioEstados.getNodeOsm(item)
            if maxlat < nodo['lat']:
                maxlat = nodo['lat']
            elif minlat > nodo['lat']:
                minlat = nodo['lat']
            if maxlon < nodo['lat']:
                maxlon = nodo['lon']
            elif minlon > nodo['lon']:
                minlon = nodo['lon']

        return distancia.dist(maxlon, maxlat, minlon, minlat)
