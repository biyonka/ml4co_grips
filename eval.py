#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:37:16 2022

@author: M. Aidli, B. Liang, E. Vercesi, A. Zhang
"""
## evaluates a bunch of configurations on a bunch of instances and save results to a csv file
import csv
import numpy as np

from utils import SCIP
from utils import Log
from ConfigSpace import Configuration
# from ConfigSpace import ConfigurationSpace

# import ConfigSpace.hyperparameters as CSH

def evaluation(instances, configurations, seeds, procedure, time_limit):
    '''
    Parameters
    ----------
    instances: file path to the instances
    configurations: list of configuration type objects
    seeds: list of seeds for SCIP
    procedure: string. example: "default", "hyperband"
    time_limit: int time limit for running SCIP (in seconds)
    
    Returns
    ---------
    A CSV file where each row is the result of running an instance with one of the configurations
    over all of the inputted seeds
    '''
    # results_as_dict = {}
    # find some way to save configuration too with the remaining results: have one method down below that could work...
    # read in each instance on the .txt file
    configs_as_dict = []
    for config in configurations:
        configs_as_dict.append(Configuration.get_dictionary(config))
        
    inst_file = open(instances, "r")
    lines = inst_file.readlines()
    inst_file.close()
    
    header = ["Instance", "Configuration_Procedure", "Primal_Dual_Integral_Percentage_Average", 
          "Primal_Dual_Integral_Percentage_Standard_Deviation"]
    name_of_file = procedure + "_Results"
    file = open(name_of_file, "w", newline = "")
    writer = csv.writer(file)
    writer.writerow(header)               
                     
    for line in lines:
        path = line.rstrip("\n")
        for configuration in configs_as_dict:
            pdi_percentage = []
            for seed in seeds:
                scip = SCIP()
                scip.write_parameter_file(D = configuration, timelimit = time_limit)
                scip.run(path = path, seed = seed) # error here: cannot find results.log
                l = Log(path = "logfile.log.gz")
                # results_as_dict[self.instance + "_Seed_" + str(seed) + "_Results"] = l.parse()
                # results_as_dict[self.instance + " Seed " + str(seed) + " Results"] = l.parse().update(configuration)
            ## compute average and standard deviation across seeds for primal-dual integral percentage
                pdi_percentage.append(l.get_primal_dual_integral()[1])
            ## now we have the primal dual integral percentage 
            average_across_seeds = np.average(pdi_percentage)
            std_across_seeds = np.std(pdi_percentage, ddof = 1)
            ## now add to CSV file!
            name = path.split("/")[-1].split(".")[0]
            data = [name, procedure, average_across_seeds, std_across_seeds]
            writer.writerow(data)
    file.close()
            
            
#TESTING
# cs = ConfigurationSpace()
# hyperparams=[
# CSH.CategoricalHyperparameter('branching/scorefunc', ['s', 'p', 'q'],default_value='q'),
# CSH.UniformFloatHyperparameter('branching/scorefac', 0, 1,default_value=0.167),
# CSH.CategoricalHyperparameter('branching/preferbinary', [True, False],default_value=False),
# CSH.UniformFloatHyperparameter('branching/clamp', 0, 0.5,default_value=0.2),
# CSH.UniformFloatHyperparameter('branching/midpull', 0, 1,default_value=0.75),
# CSH.UniformFloatHyperparameter('branching/midpullreldomtrig', 0, 1,default_value=0.5),
# CSH.CategoricalHyperparameter('branching/lpgainnormalize', ['d','l','s'],default_value='s'),
# CSH.CategoricalHyperparameter('lp/pricing', ['l','a','f','p','s','q','d'],default_value='l'),
# CSH.UniformIntegerHyperparameter('lp/colagelimit', -1, 2147483647,default_value=10),
# CSH.UniformIntegerHyperparameter('lp/rowagelimit', -1, 2147483647,default_value=10),
# CSH.CategoricalHyperparameter('nodeselection/childsel',['d','u','p','i','l','r','h'],default_value='h'),
# CSH.UniformFloatHyperparameter('separating/minortho', 0, 1,default_value=0.9),
# CSH.UniformFloatHyperparameter('separating/minorthoroot', 0, 1,default_value=0.9),
# CSH.UniformIntegerHyperparameter('separating/maxcuts', 0, 2147483647,default_value=100),
# CSH.UniformIntegerHyperparameter('separating/maxcutsroot', 0, 2147483647,default_value=2000),
# CSH.UniformIntegerHyperparameter('separating/maxroundsroot', -1, 2147483647,default_value=-1),
# CSH.UniformFloatHyperparameter('separating/minefficacyroot', 0, 1e+98,default_value=0.0001),
# CSH.UniformIntegerHyperparameter('separating/cutagelimit', -1, 2147483647,default_value=80),
# CSH.UniformIntegerHyperparameter('separating/poolfreq', -1, 65534,default_value=10),
# CSH.UniformIntegerHyperparameter('presolving/maxrounds', -1, 2147483647,default_value=-1),
# CSH.UniformFloatHyperparameter('presolving/abortfac', 0, 1,default_value=0.0008),
# CSH.UniformIntegerHyperparameter('presolving/maxrestarts', -1, 2147483647,default_value=-1)
# ]
# cs.add_hyperparameters(hyperparams)

# sample_hp1 = cs.sample_configuration()
# sample_hp2 = cs.sample_configuration()

# filepath = "SMAC/1_instances_path_test.txt"

# evaluation(instances = filepath, configurations = [sample_hp1, sample_hp2], seeds = [42, 43, 44], procedure = "test_configuration", time_limit = 60)
            