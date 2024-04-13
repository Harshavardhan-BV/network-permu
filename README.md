# network-permu
An extremely inefficient (brute-force) way to generate topo files of all n-node networks.
If you are interested in only getting the number of networks, refer to the OEIS sequence (A052283)[https://oeis.org/A052283].

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

## Verification
If you want to verify the number of networks generated, you can use the following command
```bash
python Count_verify.py
```

## Cross-check
If you have topofiles or adjacency matrices of networks and want to check if the graphs match between methods.
Edit the `Check.py` file for folder1, type1, folder2, type2. The types currently supported are `topo` and `adj` for topofiles/edgelist and adjacency matrix (csv) respectively.
Run the following command
```bash
python Check.py
```
The output will be Isographs_{folder1}_{folder2}.csv which will have the mapping of graphs between the two methods. If any graph is missing in either of the methods, it will be printed in the stdout.