#!/bin/python3

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes.update({node['id']: node})

    def node_exist(self, node_id):
        return node_id in self.nodes

    def add_edge(self, node_src, node_end, cost):
        self.nodes[node_src]['edges'].append((node_end, cost))
