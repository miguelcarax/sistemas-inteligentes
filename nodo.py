class Nodo:
    def __init__(self, padre_l, estado_l, costo_l, accion_l, profundidad_l, valor_l):
        self.padre_e = padre_l
        self.estado_e = estado_l
        self.costo_e = costo_l
        self.accion_e = accion_l
        self.profundidad_e = profundidad_l
        self.valor_e = valor_l

    def get_padre(self):
        return self.padre_e

    def get_estado(self):
        return self.estado_e

    def get_costo(self):
        return self.costo_e

    def get_accion(self):
        return self.accion_e

    def get_profundidad(self):
        return self.profundidad_e

    def get_valor(self):
        return self.valor_e

    def __repr__(self):
        #return str(self.localizacion['id']) + "por visitar: "+ str(self.lista)
        informacion = '{0}'.format(self.valor_e)
        return informacion
