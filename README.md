# Hyperparameter Optimization for SCIP using Hyperband

## [GRIPS 2022](http://www.ipam.ucla.edu/programs/student-research-programs/graduate-level-research-in-industrial-projects-for-students-grips-berlin-2022/?tab=partner)

### Students: M. AIDLI, B. Liang, [E. Vercesi](https://sites.google.com/universitadipavia.it/eleonoravercesi/home), A. Zhang 

## Instruction
This repository contains basic script to asses the performances of Hyperband, SMAC and GGA

### Set up the `conda` environmrnt 

In the main folder, run
```
 conda env create -f conda.yaml --name ml4co_grips #Replace ml4co_grips with your favourite name
 conda deactivate # Run only if you have any conda environment active
 conda activate ml4co_grips
```

### Instances
[Here](https://github.com/ds4dm/ml4co-competition/blob/main/DATA.md) you can find all the information for downloading the dataset.
Note that the dataset should go in the `./instances` folder

### Test Hyperband 

Move to the folder `hb` and run

```
python main_scip.py
```

### Test SMAC 
Move to the folder `SMAC` and run
```
python main_smacwithscip.py
```

### Test GGA
To the GGA, you firstly need a working version of [OPTANO](https://docs.optano.com/algorithm.tuner/current/userDoc/whatisalgorithmtuner.html)
Then, you can go in the folder `GGA` and run 
```
./runOptano.sh
```

### Other codes
We have also implemented a per-instance approach that strongly relies on feature extraction.
To extract feature from a bunch of instances you can use the script `get_instance_feature.py`

### Tested on

- Debian GNU/Linux 11 (bullseye)

**Note** A large portion of the Hyperband implementation was adapted from https://github.com/zygmuntz/hyperband.

### Contacts
Eleonora Vercesi : eleonora.vercesi01@universitadipavia.it
Annie Zhang : annie.zhang@uvm.edu
