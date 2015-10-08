#!/bin/python3

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        #{id : obj_node}
        self.nodes.update(node)

    def node_exist(self, node_id):
        return node_id in nodes

    def add_edge(self, node_src, node_end, cost):
        nodes[node_src]['edges'].append((node_end, cost))
