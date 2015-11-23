import espacioEstados
import estado
import distancia
import itertools

class Problema:
    valores_h = {}

    def __init__(self, estadoInicial_l, espacioEstados_l):
        self.espacioEstados_e = espacioEstados_l
        if self.espacioEstados_e.esValido(estadoInicial_l):
            self.estadoInicial_e = estadoInicial_l
        else:
            print('¡¡¡Estado No Válido!!!\nIntroduzca uno válido.')

    def esObjetivo(self, estado_l):
        return not estado_l.getLista()

    def get_estadoInicial(self):
        return self.estadoInicial_e

    def get_espacioEstados(self) :
        return self.espacioEstados_e

    def h1(self, estado):
        lonAct = estado.getLocalizacion()['lon']
        latAct = estado.getLocalizacion()['lat']
        lista = estado.getLista()
        distanciaMax = -1
        for item in lista:
            nodoDestino = self.espacioEstados_e.getNodeOsm(item)
            distanciaAux = distancia.dist(lonAct, latAct, nodoDestino['lon'], nodoDestino['lat'])
            if distanciaAux > distanciaMax:
                distanciaMax = distanciaAux

        return distanciaMax

    def h2(self, estado):
        lonAct = estado.getLocalizacion()['lon']
        latAct = estado.getLocalizacion()['lat']
        lista = estado.getLista()
        distanciaMin = 999999999
        for item in lista:
            nodoDestino = self.espacioEstados_e.getNodeOsm(item)
            distanciaAux = distancia.dist(lonAct, latAct, nodoDestino['lon'], nodoDestino['lat'])
            if distanciaAux < distanciaMin:
                distanciaMin = distanciaAux

        return distanciaMin


    def h3(self, estado):
        latAct = estado.getLocalizacion()['lat']
        lonAct = estado.getLocalizacion()['lon']
        distMax = 999999999
        # x es una tupla de un elemento que contiene una lista
        lista = estado.getLista()
        lista_codificada = estado.codificarLista()
        if lista:
            if lista_codificada not in Problema.valores_h:
                for x in itertools.permutations(lista):
                    it = 0
                    nodoDestino = self.espacioEstados_e.getNodeOsm(x[it])
                    distAux = distancia.dist(lonAct, latAct, nodoDestino['lon'], nodoDestino['lat'])
                    while it < (len(x) - 1):
                        nodoDestino1 = self.espacioEstados_e.getNodeOsm(x[it])
                        nodoDestino2 = self.espacioEstados_e.getNodeOsm(x[it + 1])
                        distAux += distancia.dist(nodoDestino1['lon'], nodoDestino1['lat'], nodoDestino2['lon'], nodoDestino2['lat'])
                        it+=1
                    if distAux < distMax:
                        distMax = distAux
                Problema.valores_h[lista_codificada] = distMax
            else:
                distMax = Problema.valores_h[lista_codificada]
        else:
            distMax = 0
            
        return distMax

    def codificarLista(self, estado):
        lista = estado.getLista()
        cadena = ''
        for item in lista:
            cadena += str(item) + '-'
        return cadena
