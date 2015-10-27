import espacioEstados
import estado

class Problema:
    def __init__(self, estadoInicial_l, espacioEstados_l):
        self.espacioEstados_e = espacioEstados
        if self.espacioEstados_e.esValido(estadoInicial_l):
            self.estadoInicial_e = estadoInicial_l
        else:
            print('Estado No Válido!!!')


    def esObjetivo(self, estado):
        return not estado.get_lista()
