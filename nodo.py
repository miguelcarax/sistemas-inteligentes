#!/usr/bin/python3

class Nodo:
    def __init__(self, id, lat, leng):
        self.id = id #Identificador del nodo
        self.coordenadas = (lat, leng) #Coordenda
        self.adyacencia = []

    def get_coord(self):
        return(self.coordenadas) #Devuelve una tupla

    def get_id(self):
        return self.id

    def coste(self):
        pass
