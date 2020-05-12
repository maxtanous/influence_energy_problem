import networkx as nx
from Cities import Cities
import matplotlib.pyplot as plt
import random
import numpy as np
import time

NODE_CITY_DICT = {
    'Boise': 0,
    'Twin  Falls':1,
    'Idaho Falls':2,
    'Rexburg':3,
    'Pocotello': 4,
    "Couer d'Alene":5,
    'Hailey':6,
    "Ketchum":7,
    "Sun Valley":8,
    "MCALL": 9,
    "Nampa": 10,
    "Meridian": 11,
    "Lewiston": 12
}

THRESHOLD_DICT = {
    'Boise': 0.335,
    'Twin  Falls': .431,
    'Idaho Falls': .392,
    'Rexburg': .431,
    'Pocotello': .0751,
    "Couer d'Alene": .4214,
    'Hailey': .3783,
    "Ketchum": .5382,
    "Sun Valley":.3708,
    "MCALL": .4322,
    "Nampa": .1678,
    "Meridian": .4251,
    "Lewiston": .2981,
}
class Graph:

    def __init__(self):
        self.network = None
        self.cities = []
        self.nodes = {}
        self.edges = {}
        self.edge_map = {}
        self.init_from_city_data()
        # Change ot build_graph_ic if running influence maximization 
        self.build_graph()

    def init_from_city_data(self):
        cities = Cities()
        self.cities = cities.cities
        self.edge_map = cities.city_neighbors

    def build_graph_ic(self):
        self.network = nx.Graph()
        counter = 0 
        for city in self.cities:
            self.network.add_node(counter, threshold=THRESHOLD_DICT[city] + .2, active=False)
            counter += 1
        edge_map = self.edge_map
        for edge in edge_map:
            for key, value in edge.items():
                key_node = NODE_CITY_DICT[key]
                print(key)
                print(key_node)
                
                for node in value:
                    self.network.add_edge(key_node,NODE_CITY_DICT[node])

    
    def build_graph(self):
        self.network = nx.Graph()
        counter = 0 
        for city in self.cities:
            print(city)
            self.network.add_node(counter)
            counter += 1
        edge_map = self.edge_map
        for edge in edge_map:
            for key, value in edge.items():
                key_node = key
                print(key)
                print(value)
                for node in value:
                    self.network.add_edge(key_node,node)

    def visualize_graph(self):
        nx.draw(self.network, with_labels=True)
        print(self.network.edges)
        plt.show()

    def IC(self,S,p,mc):
    
        self.network
        # Loop over the Monte-Carlo Simulations
        spread = []
        for i in range(mc):
            
            # Simulate propagation process      
            new_active, A = S[:], S[:]
            while new_active:
                # 1. Find out-neighbors for each newly active node
                targets = self.propagate_nx(p,new_active)
    
                #print('targets', targets)
                # 2. Determine newly activated neighbors (set seed and sort for consistency)
                np.random.seed(i)
                success =[]
                for node in targets:
                    success.append(self.activate_node(node))
                # success = np.random.uniform(0,1,len(targets)) < p
                
                new_ones = list(np.extract(success, sorted(targets)))
                # 3. Find newly activated nodes and add to the set of activated nodes
                new_active = list(set(new_ones) - set(A))
                A += new_active
                
            spread.append(len(A))
            
        return np.mean(spread)


    def greedy(self,k,p=0.1,mc=1000):
        """
        Input:  graph object, number of seed nodes
        Output: optimal seed set, resulting spread, time for each iteration
        """
        S, spread, timelapse, start_time = [], [], [], time.time()
        g = self.network
        # Find k nodes with largest marginal gain
        for _ in range(k):

            # Loop over nodes that are not yet in seed set to find biggest marginal gain
            best_spread = 0
            for j in set(range(len(g.nodes())))-set(S):
                nx.set_node_attributes(self.network, False, 'active')
                for node in S + [j]:
                    self.network.nodes[node]['active'] = True
                # Get the spread
                s = self.IC(S + [j],p,mc)
                print('spread: ', s)
                print('set: ', S + [j])
                # Update the winning node and spread so far
                if s > best_spread:
                    best_spread, node = s, j

            # Add the selected node to the seed set
            S.append(node)
            
            # Add estimated spread and elapsed time
            spread.append(best_spread)
            timelapse.append(time.time() - start_time)
        return(S,spread,timelapse)

    def propagate_nx(self,p,new_active):
        targets = []
        for node in new_active:
            targets += self.network.neighbors(node)
        return(targets)




    def activate_node(self, node):
        threshold = self.network.nodes[node]['threshold']
        active_neighbors = 0
        neighbors = self.network.neighbors(node)
        total_nieghbors = 0
        for neighbor in neighbors: 
            total_nieghbors +=1
            if self.network.nodes[neighbor]['active']:
                active_neighbors += 1
        if active_neighbors == 0:
            return False
        elif active_neighbors/total_nieghbors > threshold:
            self.network.nodes[node]['active'] = True
            return True
        else:
            return False
            
        


