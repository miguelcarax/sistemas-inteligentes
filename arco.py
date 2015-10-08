class Arco:
    def __init__(self, nodo_src, nodo_end, cost):
        self.nodo_src = nodo_src
        self.nodo_end = nodo_end
        self.cost = cost #Mirar método dentro o fuera

    def get_nodes(self):
        return (self.nodo_src, self.nodo_end)

    def get_cost(self):
        return self.cost
