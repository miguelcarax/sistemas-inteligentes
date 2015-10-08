class Edge:
    def __init__(self, node_src, node_end):
        self.node_src = nodo_src
        self.node_end = nodo_end
        self.cost = cost #Mirar método dentro o fuera

    def get_nodes(self):
        return (self.node_src, self.node_end)

    def get_cost(self):
        return self.cost
