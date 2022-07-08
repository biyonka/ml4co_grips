import pickle as pk
import sys
sys.path.insert(1, './hb/')
import utils



def eval_SCIP(instance_set, time_limit, config, outfile="eval_SCIP.csv"):
    F = open(outfile, "w+")
    for instance in instance_set:
        scip = utils.SCIP()
        scip.write_parameter_file(config, timelimit=time_limit)
        scip.run(instance, logfile=instance + ".log")
        scores = utils.Log(instance + "log.gz").parse()
        F.write(instance)
        F.write(",".join(str(x) for x in scores.values()))
        F.write("\n")
    F.close()



if __name__ == "__main__":
    ########################
    # Fix all the parameters:
    ########################

    # Select and instance set
    instance_set = []
    # TODO ?

    # Select a time limit: 10 minutes
    tl = 600

    ########################
    # Evaluate basic SCIP
    ########################
    # Eval basic SCIP
    eval_SCIP(instance_set, tl, {}, outfile="eval_basic_SCIP.csv")

    ########################
    # Evaluate HB + SCIP
    ########################
    F = open("./hb/results.pkl", "rb") # TODO, change path?
    results = pk.load(F)
    F.close()
    # Pick the configuration that minimize the loss
    losses = []
    for i, D in enumerate(results):
        losses += [(i, D['loss'])]

    best_config = next(filter(lambda x : x[1] == min([x[1] for x in losses]), losses))
    best_scip = results[best_config[0]]['params']
    # Run the code
    eval_SCIP(instance_set, tl, best_scip, outfile="eval_HB_SCIP.csv")

    ########################
    # Evaluate SMAC + SCIP
    ########################
    # TODO load the parameter obtained by SMAC
    config = {}
    eval_SCIP(instance_set, tl, {}, outfile="eval_SMAC.csv")