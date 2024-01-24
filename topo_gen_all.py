# Import packages
import os
import itertools
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import multiprocessing as mp

# Number of nodes in graph
n=5 #(change here)

# Initialize empty n node graph
G = nx.DiGraph()
G.add_nodes_from(range(0,n))

# Pandas edgelist of complete graph
df_c = nx.to_pandas_edgelist(nx.complete_graph(n,nx.DiGraph()))
df_c['type']=2

# Maximum number of edges (to permute)
m_max = n*(n-1)

# Make directories
os.makedirs('./topofiles_'+str(n)+'/', exist_ok=True)

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
                # Convert the Graph to dataframe
                df_g = nx.to_pandas_edgelist(G)
                df = df_c.copy()
                # ????
                keys = list(df_g.columns.values)
                i1 = df[keys].set_index(keys).index
                i2 = df_g.set_index(keys).index
                # Set the edge as activation if edge exists in df_g
                df.loc[i1.isin(i2),'type']=1
                # Rename nodes
                df[keys] = df[keys].applymap(lambda x: chr(ord('A') + x))
                # Save the topofile
                df.to_csv('./topofiles_'+str(n)+'/'+str(m)+'_'+str(g_n)+'.topo',sep='\t',index=False)
            g_n+=1
    return g_uniq

# Use all available cores except for two
ncores = max(mp.cpu_count() - 2, 2)
# Iterate over no. of permutations
with mp.Pool(ncores) as pool:
    bigg = pool.map(unique_graphs, range(m_max+1))
# Get the length of elements in bigg
bigg_len = [len(i) for i in bigg]
print(bigg_len)

