#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 16:29:09 2022

@author: M. Aidli, B. Liang, E. Vercesi, A. Zhang
"""
import pandas as pd

def create_training_data(instance_features_file, results_file):
    # read in instance_features_file and save it as a data frame
    # read in results_file and save it as a data frame
    instance_features_data = pd.read_csv(instance_features_file)
    # double check how the data frame for instance features is formatted
    # fix it so that the first column are the IDs!
    results_data = pd.read_csv(results_file)
    # extract the first column of instance_features_data
    instances = instance_features_data.Instance
    
    dictionary_of_results = {}
    
    for instance in instances:
        instance_results = results_data.loc[results_data['Instance'] == instance]
        instance_results_PDIP = instance_results['1_10_HB_pi_PDIP'] # change the name of this column!
        dictionary_of_results[instance] = list(instance_results_PDIP)
        
    # now create an array for the output data
    output_data = pd.DataFrame.from_dict(dictionary_of_results, orient = 'index', 
                                  columns = ["Configuration 0", "Configuration 1", "Configuration 2", 
                                             "Configuration 3", "Configuration 4", "Configuration 5",
                                             "Configuration 6", "Configuration 7", "Configuration 8",
                                             "Configuration 9"])
    return output_data
    
        
# create_training_data("1_instances_path_test_Instance_Features", "1_10_hb_pi_results.csv")
    
   
    
    
