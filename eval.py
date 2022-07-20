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
    with open(configurations, "rb") as best_configs:
        configurations = pickle.load(best_configs)
        # change this, maybe, if list of length > 1?

    inst_file = open(instances, "r")
    lines = inst_file.readlines()
    inst_file.close()

    header = ["Instance", procedure + "_PDIP",
              procedure + "_PDIP_se", procedure + "_PB", procedure + "_PB_se",
              procedure + "_DB", procedure + "_DB_se", procedure + "_PDIB", 
              procedure + "_PDIB_se"]

    name_of_file = procedure + "_results.csv"
    results_file = open(name_of_file, "w", newline="")
    writer = csv.writer(results_file)
    writer.writerow(header)
    results_file.close()
    
    just_these = lines[:3]

    for line in just_these:
        path = line.rstrip("\n")
        name = path.split("/")[-1].split(".")[0]
        for configuration in configurations:
            if 'limits/time' in configuration.keys():
                del configuration['limits/time']
            pdi_percentage = []
            primal_gap = []
            dual_gap = []
            prim_dual_gap = []
            for seed in seeds:
                scip = SCIP()
                scip.write_parameter_file(D=configuration, filename=procedure + ".set", timelimit=time_limit)
                scip.run(path=path, logfile=name + "_" + procedure + ".log", parameter_configuration=procedure + ".set",
                         seed=seed, q=False, compress_log=True)
                l = Log(path=name + "_" + procedure + ".log.gz")
                pdi_percentage.append(l.get_primal_dual_integral()[1])
                primal_gap.append(l.get_primal_bound())
                dual_gap.append(l.get_dual_bound())
                prim_dual_gap.append(l.get_gap())
                os.remove(name + "_" + procedure + ".log.gz")
                os.remove(procedure + ".set")
            avgs = [np.average(pdi_percentage), np.average(primal_gap), 
                    np.average(dual_gap), np.average(prim_dual_gap)]
            std_devs = [np.std(pdi_percentage, ddof=1), np.std(primal_gap, ddof=1), 
                        np.std(dual_gap, ddof=1), np.std(prim_dual_gap, ddof=1)]
            twice_se = []
            for std_dev in std_devs:
                twice_se.append((2 * std_dev) / np.sqrt(len(seeds)))
            data = [name]
            for i in range(len(avgs)):
                data.append(avgs[i])
                data.append(twice_se[i])
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

    evaluation(instances=filepath, configurations=config_filepath, seeds=[3, 4, 5], procedure=opt_procedure,
               time_limit=timelimit)
