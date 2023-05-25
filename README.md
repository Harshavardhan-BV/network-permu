# network-permu
An extremely inefficient (brute-force) way to generate topo files of all n-node networks

## Running the code
Change n to the desired number of nodes. This has been tested upto n=4 and the output for n=4 given in the git branch n4.
```bash
python topo_gen_all.py
```
It will iterate and output to stdout the number of networks with m permutations.
The topofiles would be stored in the directory `./topofile_n` which can be directly used with RACIPE
The figures would be stored in the directory `./figures_n`. This visualization is currently not great as the inhibitions are given as empty edges (actual network would not have any edges).
