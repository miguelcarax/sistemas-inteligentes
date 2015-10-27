import espacioEstados
import estado

class Problema:
    def __init__(self, estadoInicial, espacioEstados):
        self.estadoInicial = estadoInicial
        self.espacioEstados = espacioEstados

    def esObjetivo(self, estado):
        return not estado.get_lista()
