import os
import numpy as np
import argparse
import glob
import pandas as pd
# Parse number of nodes from command line
parser = argparse.ArgumentParser()
parser.add_argument("n", help="Number of nodes in the graph", type=int)
args = parser.parse_args()
n = args.n

def oeis_count(n):
    # Read the OEIS sequence
    oeis = pd.read_csv('b052283.txt', sep=' ', header=None, index_col=0, names=['OEIS'])
    # \sum_i=1^(n-1) n*(n-1)+1
    start_idx = 1/3*n*(n**2-3*n+5)
    end_idx = start_idx + n*(n-1)
    return oeis.loc[start_idx:end_idx].reset_index(drop=True).astype(int)

def topo_count(n):
    # List all topofiles in folder
    topo_files = glob.glob('*.topo', root_dir=f'topofiles_{n}')
    topo_files = [os.path.splitext(topo_file)[0] for topo_file in topo_files]
    # Split elements in topo_files by '_'
    topo_files = np.array([topo_file.split('_') for topo_file in topo_files], dtype=int)
    # Count the number of unique elements
    return pd.DataFrame(np.unique(topo_files[:, 0], return_counts=True), index=['m', 'topos']).T.set_index('m')

oeis = oeis_count(n)
topos = topo_count(n)
df = oeis.merge(topos, left_index=True, right_index=True, how='outer')
if any(df['OEIS'] != df['topos']):
    print('Mistmatch in count')
    print(df[df['OEIS'] != df['topos']])
else:
    print('All counts match')