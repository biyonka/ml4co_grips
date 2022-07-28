#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 13:43:42 2022

@author: M. Aidli, B. Liang, E. Vercesi, A. Zhang
"""
import networkx as nx
import numpy as np
import gurobipy
import math

from networkx.algorithms.approximation.treewidth import treewidth_min_degree
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import modularity

from encode_as_graph import Encode

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
                if self.model.getCoeff(cons, var) != 0:
                    appearance += 1 # increase value of appearance variable
                    # by 1 every time we find the variable in a constraint
            if var.Obj != 0: # if the variable appears in the obj function
            # increase appearance by 1
                appearance += 1
            appearances.append(appearance) # list of appearances for each variable
        avg_appearances = np.average(appearances)
        var_appearances = np.var(appearances, ddof = 0)
        return avg_appearances, var_appearances

    def get_num_of_constraints(self):
        return self.model.numConstrs
    
    def get_percent_equal_constraints(self): # <= and >= both are reported as < and > respectively
        freq = 0
        for constr in self.model.getConstrs():
            if constr.Sense == '=':
                freq += 1
        return ((freq / self.model.numConstrs) * 100)
    
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
        return {
            "Number of Variables": self.get_num_of_vars(),
            "Average of Variable Ranges": self.get_range_of_vars_stats()[0],
            "Median of Variable Ranges": self.get_range_of_vars_stats()[1],
            "Variance of Variable Ranges": self.get_range_of_vars_stats()[2],
            "Average Number of Variable Appearances": self.get_node_appear()[0],
            "Variance of Number of Variable Appearances": self.get_node_appear()[1],
            "Number of Constraints": self.get_num_of_constraints(),
            "Percent of Equality Constraints": self.get_percent_equal_constraints(),
            "Coefficient Average": self.get_coeff_avg_var()[0],
            "Coefficient Variance": self.get_coeff_avg_var()[1],
            "Variables over Constraints": self.get_division() 
        }
    
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
    
    def get_transitivity(self): # this will always be 0 because we have a bipartite graph!
        transitivity = nx.transitivity(self.graph)
        return transitivity
    
    def all_features(self):
        return {
            "Graph Density": self.get_density(),
            "Graph Treewidth": self.get_treewidth(),
            "Graph Modularity": self.get_modularity(),
            "Graph Transitivity": self.get_transitivity(),
        }
    
# test_graph = Encode("../instances/1_item_placement/testing/item_placement_0.mps.gz")
# encoded_as_graph = test_graph.encode_as_graph()
# to_extract = Graph_Extractor(encoded_as_graph)
# to_extract.get_density()
# to_extract.get_treewidth()
# to_extract.get_modularity()
# to_extract.get_transitivity()

    
