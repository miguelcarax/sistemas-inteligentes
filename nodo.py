class Nodo:
    def __init__(self, padre_l, estado_l, costo_l, accion_l, profundidad_l, valor_l):
        self.padre = padre_l
        self.estado = estado_l
        self.costo = costo_l
        self.accion = accion_l
        self.profundidad = profundidad_l
        self.valor = valor_l

    def __repr__(self):
        informacion = '{0}'.format(self.valor)
        return informacion

    def __lt__(self, other):
        return self.valor < other.valor
