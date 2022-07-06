# ml4co_grips

## Set up the `conda` environmrnt

In the main folder, run
```
 conda env create -f conda.yaml --name ml4co_grips #Replace ml4co_grips with your favourite name
 conda deactivate # Run only if you have any conda environment active
 conda activate ml4co_grips
```

Move to the folder `hb` and run

```
python main_scip.py
```
**Tested on**

- Debian GNU/Linux 11 (bullseye)

**Note** A large portion of the Hyperband implementation was adapted from https://github.com/zygmuntz/hyperband.
