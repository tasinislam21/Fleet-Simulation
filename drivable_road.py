import random
import networkx as nx

class DrivableRoad(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DrivableRoad, cls).__new__(cls)
        return cls.instance

    def set_graph(self, graph):
        self.graph = graph
        self.list_of_nodes = list(graph.nodes)

    def set_node_positions(self, node_positions):
        self.node_positions = node_positions

    def get_random_node(self):
        return random.choice(self.list_of_nodes)

    def get_path(self, source, target):
        path_coords = []
        route = nx.shortest_path(self.graph, source, target, weight="length")
        for i in route:
            path_coords.append(self.node_positions.get(i))
        return path_coords