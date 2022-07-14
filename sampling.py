'''
Stratified sample ancording to a certain feature
@author M. AIDLI, G. Iommazzo, B. Liang, E. Vercesi, A. Zhang
'''
import os
import numpy as np
from utils import *
import argparse
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import time
from collections import Counter

def write_file(family, set_of_instances, file_name, with_classes=False, y=None):
    F = open(file_name, "w+")
    for i, f in enumerate(set_of_instances):
        F.write("../instances/{}_{}/train/{}_{}.mps.gz".format(num_dataset[family], family, family, f))
        if with_classes:
            k = list(names).index(f)
            F.write(",{}".format(y[k]))
        F.write("\n")
    F.close()

def old_stratify():
    start = time.time()
    while len(names) < args.s:
        # Pick one instance
        i = np.random.randint(0, len(files))
        file = files[i]
        # Verify wether the instance is in the folder
        if "{}_{}_3.log.gz".format(args.p, i) in files:
            # Split the name of the file, retrieve the number
            numb = file.split("_")[2]
            # If the number is not in the list name, collect the associated score
            if numb not in names:
                score = 0
                try:  # Collect score only if you have three run on three different seeds
                    for seed in [3, 4, 5]:
                        score += Log(directory + "item_placement_{}_{}.log.gz".format(i, seed)).parse()[args.hm]
                    scores.append(score / 3)
                    names.append(numb)
                except:
                    pass
    print("Time for collecting a random sampling:", time.time() - start)

    ######################################
    # Stratify
    ######################################
    # Create three bins among min score and max score
    bins = np.linspace(min(scores), max(scores), 3)
    # Return the indices of the bins to which each value in input array belongs
    y_binned = np.digitize(scores, bins)
    # Print info on the created classes
    counter_classes = Counter(y_binned)
    for k in counter_classes.keys():
        print("Class", k, ":", counter_classes[k], "elements", flush=True)


if __name__ == "__main__":
    ##################
    # Parser
    ##################
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", metavar='d', help="Name of the directory with the log files under study")
    parser.add_argument("-s", metavar='s', help="Sample size you want to extract (Train size + Test size)", type=int)
    parser.add_argument("-r", metavar='r', help="Percentage of test set on total sample dimension", type=float)
    parser.add_argument("-p", metavar='p', help="Problem name: one among item_placement, load_balancing, anonymous", type=str, default="item_placement")
    parser.add_argument("-hm", metavar='hm', help="Measure of hardness to be collected and to cluster on", default="Primal-Dual Integral Percentage")
    args = parser.parse_args()
    directory = args.d
    try:
        # Basic check of the passed directory name
        assert directory[-1] in ["/", "\\"]
    except:
        raise ValueError("Directory path should end with / or \\")


    # Store the name of the instance family in a variable
    family = args.p
    hm = args.hm
    sample_size = args.s
    train_test_percentage = args.r

    # Associate dataset name to a number
    num_dataset = {'item_placement': "1"}

    ######################################
    # Collect one score for each instance
    ######################################
    # Note: some of the following passages can be avoided in case of complete exploration
    names = [] # Name of the instance
    scores = [] # Score to be collected
    files = os.listdir(directory)

    for file in files:
        # Split the name of the file, retrieve the number
        numb = file.split("_")[2]
        # Verify wether the instance is in the folder
        if "{}_{}_3.log.gz".format(family, numb) in files:
            # If the number is not in the list name, collect the associated score
            if numb not in names:
                score = 0
                cont = 0
                for seed in [3, 4, 5]:
                    try:
                        score_this = Log(directory + "item_placement_{}_{}.log.gz".format(numb, seed)).parse()[hm]
                        if score_this != float('inf'):
                            cont += 1
                            score += score_this
                    except:
                        pass
                if cont > 0:
                    scores.append(score /cont)
                    names.append(numb)


    #############
    # KMeans
    #############
    kmeans = KMeans(n_clusters=3, random_state=10).fit(np.asarray(scores).reshape(-1, 1))
    y_cluster = kmeans.labels_

    counter_classes = Counter(y_cluster)
    for k in counter_classes.keys():
        print("Class", k, ":", counter_classes[k], "elements", flush=True)

    ###############
    # Stratify
    ##############
    percentage = [counter_classes[k]/sum([counter_classes[k] for k in counter_classes.keys()])
                  for k in counter_classes.keys()]

    probability_of_each_element = [percentage[k] for k in y_cluster]
    p = [x / sum(probability_of_each_element) for x in probability_of_each_element]

    sample = np.random.choice(names, sample_size, p=p, replace=False)


    ######################################
    # Divide between train and test
    ######################################
    Xtr, Xte = train_test_split(sample, test_size=train_test_percentage)

    print("Files for the training set:", len(Xtr), flush=True)
    print("Files for the test set:", len(Xte), flush=True)

    number = num_dataset[family]
    write_file(family, Xtr, "./SMAC/{}_instance_path_train.txt".format(number))
    write_file(family, Xte, "./SMAC/{}_instance_path_test.txt".format(number))
    write_file(family, Xtr, "./hb/{}_instance_path_train_with_classes.txt".format(number), with_classes=True, y = y_cluster)
    write_file(family, Xte, "./hb/{}_instance_path_test_with_classes.txt".format(number), with_classes=True, y=y_cluster)