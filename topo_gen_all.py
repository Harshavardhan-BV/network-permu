# Import packages
import os
import itertools
import numpy as np
import pandas as pd
import networkx as nx
import multiprocessing 

# Number of nodes in graph
n=4 #(change here)

# Initialize empty n node graph
G = nx.DiGraph()
G.add_nodes_from(range(0,n))

# Get the unique graphs graphs with m edges network and p positive edges
def unique_graphs(m,p,save_topo=True):
    # generate all possible pairs of nodes
    node_pairs = list(itertools.product(range(0, n), repeat=2))
    # create all possible permutations of n edges
    edge_permutations = list(itertools.combinations(node_pairs, m))
    # +ve edges
    p_edge_permutations = list(itertools.combinations(range(m),p))
    # create a list of graphs with each permutation of edges
    g_uniq = []
    g_n=0
    for p_edge in p_edge_permutations:
        #change weights of edges
        weights = [1 if i in p_edge else 2 for i in range(0,m)]
        for edges in edge_permutations:
            G1 = G.copy()
            for i in range(len(edges)):
                G1.add_edge(edges[i][0],edges[i][1],weight=weights[i])
            for G2 in g_uniq:
            # if the graph is isomorphic to existing do nothing
                if nx.algorithms.is_isomorphic(G1, G2, edge_match=nx.algorithms.isomorphism.numerical_edge_match('weight', 1)):
                    break
            else:
                # or add it to unique list
                g_uniq.append(G1)
                if save_topo:
                    # Convert the Graph to dataframe
                    df = nx.to_pandas_edgelist(G1)
                    # Rename nodes
                    keys = ['source','target']
                    # convert number to letters
                    df[keys] = df[keys].applymap(lambda x: chr(ord('A') + x))
                    # Save the topofile
                    df.to_csv('./topofiles_'+str(n)+'/'+str(m)+'_'+str(p)+'_'+str(g_n)+'.topo',sep='\t',index=False)
                    g_n+=1
    return g_uniq

# Maximum number of edges (to permute)
m_max = n**2
# Make directories
os.makedirs('./topofiles_'+str(n)+'/')

# Use all available cores except for two
ncores = max(multiprocessing.cpu_count() - 2, 2)
# Iterate over no. of permutations
with multiprocessing.Pool(ncores) as pool:
    pool.starmap(unique_graphs, [(m, p) for m in range(m_max+1) for p in range(0, m+1)])