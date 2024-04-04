# Import packages
import os
import argparse
import itertools
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import multiprocessing as mp

# Number of nodes in graph from command line
parser = argparse.ArgumentParser()
parser.add_argument("n", help="Number of nodes in the graph", type=int)
args = parser.parse_args()
n = args.n

# Initialize empty n node graph
G = nx.DiGraph()
G.add_nodes_from(range(0,n))

# Pandas edgelist of complete graph
df_c = nx.to_pandas_edgelist(nx.complete_graph(n,nx.DiGraph()))

# Maximum number of edges (to permute)
m_max = (n*(n-1))//2

# Make directories
os.makedirs('./topofiles_'+str(n)+'/', exist_ok=True)

def topo_conv(G1, m, g_n, d_type=2):
    m = m if d_type==2 else n*(n-1)-m
    # Convert the "unique" Graph to dataframe
    df_g = nx.to_pandas_edgelist(G1)
    # Start with the complete graph
    df = df_c.copy()
    df['type']=d_type
    keys = ['source','target']
    # Convert source, target to keys for complete graph
    i1 = df[keys].set_index(keys).index
    # Do the same for the unique graph
    i2 = df_g.set_index(keys).index
    # Set the edge as activation if edge exists in df_g
    df.loc[i1.isin(i2),'type'] = 1 if d_type==2 else 2
    # Rename nodes
    df[keys] = df[keys].map(lambda x: chr(ord('A') + x))
    # Save the topofile
    df.to_csv('./topofiles_'+str(n)+'/'+str(m)+'_'+str(g_n)+'.topo',sep='\t',index=False)

# Select the unique graphs with m edges network (ie do not repeat isomorphic ones) 
def unique_graphs(m, save_topo=True):
    # generate all possible pairs of nodes
    node_pairs = itertools.product(range(0, n), repeat=2)
    # filter out self-loops
    node_pairs = filter(lambda x: x[0] != x[1], node_pairs)
    # create all possible permutations of m edges
    edge_permutations = itertools.combinations(node_pairs, m)
    # create a list of graphs with each permutation of edges
    g_uniq = []
    g_n = 0
    for edges in edge_permutations:
        G1 = G.copy()
        G1.add_edges_from(edges)
        for G2 in g_uniq:
            # if the graph is isomorphic to existing do nothing
            if nx.algorithms.is_isomorphic(G1, G2):
                break
        else:
            # or add it to unique list
            g_uniq.append(G1)
            if save_topo:
                topo_conv(G1, m, g_n)
                if m!=m_max:
                    topo_conv(G1, m, g_n, d_type=1)
            g_n+=1
    return g_uniq

# Use all available cores except for two
ncores = max(mp.cpu_count() - 2, 2)
# Iterate over no. of permutations
with mp.Pool(ncores) as pool:
    bigg = pool.map(unique_graphs, range(m_max+1))
# Get the length of elements in bigg
bigg_len = [len(i) for i in bigg]
# Exploiting the symmetry
bigg_len = bigg_len + bigg_len[-2::-1]
print(bigg_len, sum(bigg_len))

