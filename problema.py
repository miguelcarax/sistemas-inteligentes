import frontera

class Problema:
    def __init__(self, estadoInicial):
        self.estadoInicial = estadoInicial
        self.frontera = Frontera()
        self.frontera.insertar({'padre':{}, 'estado' = self.estadoInicial, 'costo' = 0, 'accion' = '', 'profundidad' = 0, 'valor' = 0})

    def esObjetivo(self, estado):
        return not estado.get_lista()
