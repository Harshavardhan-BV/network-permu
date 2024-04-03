# network-permu
An extremely inefficient (brute-force) way to generate topo files of all n-node networks

## Running the code
Install the required packages using the following command
```bash
pip install -r requirements.txt
```
Change n to the desired number of nodes. This has been tested upto n=5 and the output for n=4 given in the git branch n4.
```bash
python topo_gen_all.py <number of nodes>
```
It will iterate and output to stdout the number of networks with m permutations.
The topofiles would be stored in the directory `./topofile_n` which can be directly used with RACIPE.
