#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 13:43:42 2022

@author: M. Aidli, B. Liang, E. Vercesi, A. Zhang
"""

import networkx as nx

from networkx.algorithms.approximation.treewidth import treewidth_min_degree
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import modularity

class Extractor:
    def __init__(self, graph):
        self.graph = graph
        
    def get_density(self):
        density = nx.density(self.graph)
        return density
    
    def get_treewidth(self):
        tw, tree = treewidth_min_degree(self.graph)
        return tw
    
    def get_modularity(self):
        best_comms = greedy_modularity_communities(self.graph)
        best_comms_as_lists = [list(comm) for comm in best_comms]
        mod = modularity(self.graph, best_comms_as_lists)
        return mod
    
    def get_transitivity(self):
        transitivity = nx.transitivity(self.graph)
        return transitivity
    
    def get_eigenvector_centrality(self):
        nodes_and_centralities = nx.eigenvector_centrality(self.graph)
        centralities = []
        for node in nodes_and_centralities.keys():
            centralities.append(nodes_and_centralities[node])
        return centralities
    
    def all_features(self):
        return {
            "Density": self.get_density(),
            "Treewidth": self.get_treewidth(),
            "Modularity": self.get_modularity(),
            "Transitivity": self.get_transitivity(),
            "Eigenvector Centrality": self.get_eigenvector_centrality() 
        }
    
# TESTING
# test_graph = nx.complete_multipartite_graph(10, 15)

# extract = Extractor(test_graph)
# extract.all_features()