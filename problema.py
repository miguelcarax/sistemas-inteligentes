import espacioEstados
import estado

class Problema:
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
