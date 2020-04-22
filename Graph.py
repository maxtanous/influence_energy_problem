import networkx as nx
from Cities import Cities
import matplotlib.pyplot as plt


class Graph:

    def __init__(self):
        self.network = None
        self.cities = []
        self.nodes = {}
        self.edges = {}
        self.edge_map = {}
        self.init_from_city_data()
        self.build_graph()

    def init_from_city_data(self):
        cities = Cities()
        self.cities = cities.cities
        self.edge_map = cities.city_neighbors

    
    def build_graph(self):
        self.network = nx.Graph()
        for city in self.cities:
            self.network.add_node(city)
        edge_map = self.edge_map
        for edge in edge_map:
            for key, value in edge.items():
                key_node = key
                for node in value:
                    self.network.add_edge(key_node,node)

    def visualize_graph(self):
        nx.draw(self.network, with_labels=True)
        plt.show()
            
        

graph = Graph()
graph.visualize_graph()