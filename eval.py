#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:37:16 2022

@author: M. Aidli, B. Liang, E. Vercesi, A. Zhang
"""
## evaluates a bunch of configurations on a bunch of instances and save results to a csv file
import csv
import os

import numpy as np
import pickle
import argparse
import sys

sys.path.append("../")

from utils import SCIP
from utils import Log


def evaluation(instances, configurations, seeds, procedure, time_limit):
    '''
    Parameters
    ----------
    instances: file path to the instances
    configurations: pickle type object that contains a list of configs, file name ends in .pkl
    seeds: list of seeds for SCIP
    procedure: string. example: "hyperband"
    time_limit: int time limit for running SCIP (in seconds)

    Returns
    ---------
    A CSV file where each row is the result of running an instance with one of the configurations
    over all of the inputted seeds
    '''
    # results_as_dict = {}
    # find some way to save configuration too with the remaining results: have one method down below that could work...
    with open(configurations, "rb") as best_configs:
        configurations = pickle.load(best_configs)
        # change this, maybe, if list of length > 1?

    inst_file = open(instances, "r")
    lines = inst_file.readlines()
    inst_file.close()

    header = ["Instance", "PDI_Percentage_Average",
              "PDI_Percentage_Two_Std_Error"]

    name_of_file = procedure + "_results.csv"
    results_file = open(name_of_file, "w", newline="")
    writer = csv.writer(results_file)
    writer.writerow(header)
    results_file.close()

    for line in lines:
        path = line.rstrip("\n")
        name = path.split("/")[-1].split(".")[0]
        for configuration in configurations:
            if 'limits/time' in configuration.keys():
                del configuration['limits/time']
            pdi_percentage = []
            for seed in seeds:
                scip = SCIP()
                scip.write_parameter_file(D=configuration, filename=procedure + ".set", timelimit=time_limit)
                scip.run(path=path, logfile=name + "_" + procedure + ".log", parameter_configuration=procedure + ".set",
                         seed=seed, q=False, compress_log=True)
                l = Log(path=name + "_" + procedure + ".log.gz")
                ## compute average and standard deviation across seeds for primal-dual integral percentage
                pdi_percentage.append(l.get_primal_dual_integral()[1])
                os.remove(name + "_" + procedure + ".log.gz")
            ## now we have the primal dual integral percentage
            average_across_seeds = np.average(pdi_percentage)
            std_across_seeds = np.std(pdi_percentage, ddof=1)
            twice_se_across_seeds = (2 * std_across_seeds) / np.sqrt(len(seeds))
            ## now add to CSV file!
            data = [name, average_across_seeds, twice_se_across_seeds]
            results_file = open(name_of_file, "a")
            writer = csv.writer(results_file)
            writer.writerow(data)
            results_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", metavar='c', help=".pkl file containing a list of configurations", type=str)
    parser.add_argument("-f", metavar='f', help="file with list of instances", type=str)
    parser.add_argument("-t", metavar='t', help="time limit for SCIP", type=int)
    parser.add_argument("-p", metavar='p', help="optimization procedure (ex: hyperband, SMAC)", type=str)

    args = parser.parse_args()

    config_filepath = args.c
    filepath = args.f
    timelimit = args.t
    opt_procedure = args.p

    # TESTING

    # filepath = "SMAC/1_instances_path_test.txt"
    # config_filepath = "/home/azhang/Downloads/hb_best_config.pkl"

    evaluation(instances=filepath, configurations=config_filepath, seeds=[3, 4, 5], procedure=opt_procedure,
               time_limit=timelimit)
