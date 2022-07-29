#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 15:58:37 2022

@author: M. Aidli, B. Liang, E. Vercesi, A. Zhang
"""
import networkx as nx
import gurobipy
import math

# from gurobipy import GRB

class Encode:
    def __init__(self, file_path):
        self.model = gurobipy.read(file_path)
        
    def encode_as_graph(self):
        G = nx.Graph()
        
        variables = []
        constraints = []
        weighted_edges = []
        for var in self.model.getVars():
            var_attr = {"Lower Bound": var.LB}
            if math.isinf(var.LB) == True:
                var_attr["Has Lower Bound"] = 0
            else:
                var_attr["Has Lower Bound"] = 1
            var_attr["Upper Bound"] = var.UB
            if math.isinf(var.UB) == True:
                var_attr["Has Upper Bound"] = 0
            else:
                var_attr["Has Upper Bound"] = 1
            var_attr["Objective Coefficient"] = var.Obj
            if var.Vtype == 'C':
                var_attr["Is Binary"] = 0
                var_attr["Is Continuous"] = 1
                var_attr["Is Integer"] = 0
            elif var.Vtype == 'B':
                var_attr["Is Binary"] = 1
                var_attr["Is Continuous"] = 0
                var_attr["Is Integer"] = 0
            elif var.Vtype == 'I':
                var_attr["Is Binary"] = 0
                var_attr["Is Continuous"] = 0
                var_attr["Is Integer"] = 1
            variables.append((var.varName, var_attr))
            for constr in self.model.getConstrs():
                constraints.append((constr.constrName, {"RHS": constr.RHS}))
                if self.model.getCoeff(constr, var) != 0:
                    weighted_edges.append((constr.constrName, var.VarName, self.model.getCoeff(constr, var)))
            
        all_nodes = [*variables, *constraints]
        G.add_nodes_from(all_nodes)
        G.add_weighted_edges_from(weighted_edges, weight = "Coefficient of Variable in Constraint")
        
        return G
            
        
        
      
        
        
    # def encode_as_graph(self):
    #     nodes = self.model.getVars()
    #     node_attributes = []
    #     constraints = self.model.getConstrs()
    #     constraint_attributes = []
    #     weighted_edges = []
    #     for v in self.model.getVars():
    #         node_attr = {}
    #         node_attr["Lower Bound"] = v.LB
    #         if math.isinf(v.LB) == True: 
    #             node_attr["Has Lower Bound"] = 0
    #         else:
    #             node_attr["Has Lower Bound"] = 1
    #         node_attr["Upper Bound"] = v.UB
    #         if math.isinf(v.UB) == True:
    #             node_attr["Has Upper Bound"] = 0
    #         else:
    #             node_attr["Has Upper Bound"] = 1
    #         node_attr["Objective Coefficient"] = v.Obj
            # if v.Vtype == 'C':
            #     node_attr["Is Binary"] = 0
            #     node_attr["Is Continuous"] = 1
            #     node_attr["Is Integer"] = 0
            # elif v.Vtype == 'B':
            #     node_attr["Is Binary"] = 1
            #     node_attr["Is Continuous"] = 0
            #     node_attr["Is Integer"] = 0
            # elif v.Vtype == 'I':
            #     node_attr["Is Binary"] = 0
            #     node_attr["Is Continuous"] = 0
            #     node_attr["Is Integer"] = 1
    #         node_attributes.append(node_attr)
    #         for c in self.model.getConstrs():
    #             constr_attr = {}
    #             constr_attr["Right Hand Side"] = c.RHS
    #             constraint_attributes.append(constr_attr)
    #             if self.model.getCoeff(c, v) != 0:
    #                 weighted_edges.append((c, v, self.model.getCoeff(c, v)))
        
        # G = nx.Graph()
        # for (node, node_attribute) in zip(nodes, node_attributes):
        #     G.add_nodes_from([(node, node_attribute)])
        # for (constraint, constraint_attribute) in zip(constraints, constraint_attributes):
        #     G.add_nodes_from([(constraint, constraint_attribute)])
        # for weighted_edge in weighted_edges:
        #     G.add_weighted_edges_from([weighted_edge])
        
