import random
import networkx as nx
import osmnx as ox

class DrivableRoad(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DrivableRoad, cls).__new__(cls)
        return cls.instance

    def set_graph(self, graph):
        self.graph = graph
        _, self.edges = ox.graph_to_gdfs(graph, nodes=True, edges=True)
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

    def get_max_speed(self, start_node, end_node):
        edge = self.edges.loc[
            self.edges.index.get_level_values(0).isin([start_node]) &
            self.edges.index.get_level_values(1).isin([end_node])
            ]
        return int((edge.maxspeed.item())[:-4])