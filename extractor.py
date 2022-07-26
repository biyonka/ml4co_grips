#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 13:43:42 2022

@author: M. Aidli, B. Liang, E. Vercesi, A. Zhang
"""

# update this to extract features from the MILP as well!

import networkx as nx
import numpy as np
import gurobipy
import math

from networkx.algorithms.approximation.treewidth import treewidth_min_degree
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import modularity

class Instance_Extractor:
    def __init__(self, file_path):
        self.model = gurobipy.read(file_path)
        
    def get_num_of_vars(self):
        return self.model.numVars
    
    def get_range_of_vars_stats(self):
        range = []
        for var in self.model.getVars():
            if math.isinf(var.UB) or math.isinf(var.LB) == True:
                continue
            range.append(var.UB - var.LB)
        average_range = np.average(range)
        median_range = np.median(range)
        variance_range = np.var(range, ddof = 0)
        return average_range, median_range, variance_range
    
    def get_node_appear(self):
        appearances = []
        for var in self.model.getVars():
            appearance = 0
            for cons in self.model.getConstrs():
                if np.abs(self.model.getCoeff(cons, var)) > 0:
                    appearance += 1 # increase value of appearance variable
                    # by 1 every time we find the variable in a constraint
            if np.abs(var.Obj) > 0: # if the variable appears in the obj function
            # increase appearance by 1
                appearance += 1
            appearances.append(appearance) # list of appearances for each variable
        avg_appearances = np.average(appearances)
        var_appearances = np.var(appearances, ddof = 0)
        return avg_appearances, var_appearances

    def get_num_of_constraints(self):
        return self.model.numConstrs
    
    def get_num_equal_constraints(self): # <= and >= both are reported as < and > respectively
        freq = 0
        for constr in self.model.getConstrs():
            if constr.Sense == '=':
                freq += 1
        return freq
    
    def get_coeff_avg_var(self): 
        coeffs = []
        for var in self.model.getVars():
            for cons in self.model.getConstrs():
                if self.model.getCoeff(cons, var) != 0:
                    coeffs.append(self.model.getCoeff(cons, var))
            if var.Obj != 0:
                coeffs.append(var.Obj)
        avg_coeffs = np.average(coeffs)
        var_coeffs = np.var(coeffs, ddof = 0)
        return avg_coeffs, var_coeffs
    
    def get_division(self):
        return (self.model.numVars / self.model.numConstrs)
    
    def all_inst_features(self):
        range_stats = self.get_range_of_vars_stats()
        node_appear_stats = self.get_node_appear()
        coeff_stats = self.get_coeff_avg_var()
        features = []
        features.append(self.get_num_of_vars())
        for stat in range_stats:
            features.append(stat)
        for stat in node_appear_stats:
            features.append(stat)
        features.append(self.get_num_of_constraints())
        features.append(self.get_num_equal_constraints())
        for stat in coeff_stats:
            features.append(stat)
        features.append(self.get_division())
        
        return features
    
class Graph_Extractor:
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
        graph_features = [self.get_density(), self.get_treewidth(), self.get_modularity(),
                          self.get_transitivity()]
        for cent in self.get_eigenvector_centrality():
            graph_features.append(cent)
        return graph_features
    
# TESTING
test_graph = nx.complete_multipartite_graph(10, 15)

extract = Graph_Extractor(test_graph)
extract.all_features()

# toy_example = Instance_Extractor("../instances/1_item_placement/one/item_placement_0.mps.gz")
# toy_example.all_inst_features()
# m = gurobipy.Model("mip1")

# x = m.addVar(vtype = GRB.BINARY, name = "x")
# y = m.addVar(vtype = GRB.BINARY, name = "y")
# z = m.addVar(vtype = GRB.BINARY, name = "z")

# m.setObjective(x + y + z, GRB.MAXIMIZE)

# m.addConstr(x + 2 * y + 3 * z <= 4, "c0")
# m.addConstr(x + y >= 1, "c1")

