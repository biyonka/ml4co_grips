#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 10:13:30 2022

@author: M. Aidli, B. Liang, E. Vercesi, A. Zhang
"""
from encode_as_graph import Encode
from extractor import Instance_Extractor
from extractor import Graph_Extractor
import csv
import argparse

# read in instances - save the output to a csv file

def get_all_features(file_path, purpose):
    '''
    Parameters
    ----------
    file_path : file path to instances
    purpose : string. example: "Training", "Validation"
    
    Returns
    -------
    CSV file with instance features

    '''
    inst_file = open(file_path, "r")
    lines = inst_file.readlines()
    inst_file.close()
    
    header = ["Instance", "Number of Variables", "Average of Variable Ranges", 
              "Median of Variable Ranges", "Variance of Variable Ranges", 
              "Average Number of Variable Appearances", "Variance of Number of Variable Appearances",
              "Number of Constraints", "Percent of Equality Constraints", "Coefficient Average",
              "Coefficient Variance", "Variables over Constraints", "Graph Density",
              "Graph Treewidth", "Graph Modularity", "Graph Transitivity"]

    file_name = purpose + "_Instance_Features"
    features_file = open(file_name, "w", newline = "")
    writer = csv.writer(features_file)
    writer.writerow(header)
    features_file.close()
    
    just_these_lines = lines[:4]
    
    for line in just_these_lines:
    
        instance_name = line.split("/")[-1].split(".")[0]
    
        model = Encode(line)
        G = model.encode_as_graph()
    
        extract_from_G = Graph_Extractor(G)
        graph_feats = extract_from_G.all_features()
    
        extract_from_inst = Instance_Extractor(line)
        inst_feats = extract_from_inst.all_inst_features()
    
        all = {"Instance": instance_name, **inst_feats, **graph_feats}
    
        features_file = open(file_name, "a")
        writer = csv.DictWriter(features_file, all.keys())
        writer.writerow(all)
        features_file.close()
    
if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", metavar = "f", help = "file path to instances", type = str)
    parser.add_argument("-p", metavar = "p", help = "a string like 'training' or 'validation'", type = str)
    
    args = parser.parse_args()
    
    file = args.f
    purpose = args.p
    
    get_all_features(file_path = file, purpose = purpose)
    
    