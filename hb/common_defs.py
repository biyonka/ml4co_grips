"imports and definitions shared by various defs files"

import numpy as np

from math import sqrt
from time import time
from pprint import pprint

from sklearn.metrics import roc_auc_score as AUC, log_loss, accuracy_score as accuracy
from sklearn.metrics import mean_squared_error as MSE  # mean_absolute_error as MAE

from hyperopt import hp
from hyperopt.pyll.stochastic import sample
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import utils
import subprocess


# handle floats which should be integers
# works with flat params
def handle_integers(params):
    new_params = {}
    for k, v in params.items():
        if type(v) == float and int(v) == v:
            new_params[k] = int(v)
        else:
            new_params[k] = v

    return new_params


###

def train_and_eval_sklearn_classifier(clf, data):
    x_train = data['x_train']
    y_train = data['y_train']

    x_test = data['x_test']
    y_test = data['y_test']

    clf.fit(x_train, y_train)

    try:
        p = clf.predict_proba(x_train)[:, 1]  # sklearn convention
    except IndexError:
        p = clf.predict_proba(x_train)

    ll = log_loss(y_train, p)
    auc = AUC(y_train, p)
    acc = accuracy(y_train, np.round(p))

    print("\n# training | log loss: {:.2%}, AUC: {:.2%}, accuracy: {:.2%}".format(ll, auc, acc))

    #

    try:
        p = clf.predict_proba(x_test)[:, 1]  # sklearn convention
    except IndexError:
        p = clf.predict_proba(x_test)

    ll = log_loss(y_test, p)
    auc = AUC(y_test, p)
    acc = accuracy(y_test, np.round(p))

    print("# testing  | log loss: {:.2%}, AUC: {:.2%}, accuracy: {:.2%}".format(ll, auc, acc))

    # return { 'loss': 1 - auc, 'log_loss': ll, 'auc': auc }
    return {'loss': ll, 'log_loss': ll, 'auc': auc}


###

# "clf", even though it's a regressor
def train_and_eval_sklearn_regressor(clf, data):
    x_train = data['x_train']
    y_train = data['y_train']

    x_test = data['x_test']
    y_test = data['y_test']

    clf.fit(x_train, y_train)
    p = clf.predict(x_train)

    mse = MSE(y_train, p)
    rmse = sqrt(mse)
    # mae = MAE( y_train, p )

    print("\n# training | RMSE: {:.4f}".format(rmse))

    #

    p = clf.predict(x_test)

    mse = MSE(y_test, p)
    rmse = sqrt(mse)
    # mae = MAE( y_test, p )

    print("# testing  | RMSE: {:.4f}".format(rmse))

    return {'loss': rmse, 'rmse': rmse}


def run_and_eval_scip(config, list_of_instances):
	keys = ["Primal-Dual Integral Value", "Primal-Dual Integral Percentage",
			"Gap", "Time First Feasible", "Primal Bound", "Dual Bound", "B&B Tree nodes",
			"Time to Solve Root Node", "Number of LP Iterations", "Total Time"]
	out = dict(zip(keys, [[] for _ in keys]))
	# Loop on all the files
	for file in list_of_instances:
		# Open a temporary file in which add the SCIP parameter
		F = open("scip_temp.set", "w+")
		# For each parameter in the config dic, write the parameter and the value in the scip_temp.set file
		for param in config.keys():
			F.write(param)
			F.write(" = ")
			F.write(str(config[param]))
			F.write("\n")
		F.close()
		# Run SCIP with the desired setting of parameters and a file as a log
		subprocess.run("scip -f {} -l {} -s scip_temp.set -q".format(file, file + ".log"), shell=True)
		# Retrieve the info on the SCIP run
		scores = utils.Log(file + ".log").parse()
		# append the score on the list out
		for k in scores.keys():
			out[k].append(scores[k])
		# Remove no more useful file
		os.remove(file + ".log")
		os.remove("scip_temp.set")
	return out
