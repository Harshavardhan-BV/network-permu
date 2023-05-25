# Import packages
import os
import itertools
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Initialize empty n node graph
n=4
G = nx.DiGraph()
G.add_nodes_from(range(0,n))

# Get all possible graphs with m edges network
def get_possible_edges(m):
    # generate all possible pairs of nodes
    node_pairs = itertools.product(range(0, n), repeat=2)
    # filter out self-loops
    node_pairs = filter(lambda x: x[0] != x[1], node_pairs)
    # create all possible permutations of n edges
    edge_permutations = itertools.combinations(node_pairs, m)
    # create a list of graphs with each permutation of edges
    graphs = []
    for edges in edge_permutations:
        G1 = G.copy()
        G1.add_edges_from(edges)
        graphs.append(G1)
    return graphs

# Select the unique graphs (ie do not repeat isomorphic ones)
def unique_graphs(m):
    # get all combinations with m edges
    gs = get_possible_edges(m)
    g_uniq=[]
    for G1 in gs:
        for G2 in g_uniq:
            # if the graph is isomorphic to existing do nothing
            if nx.algorithms.is_isomorphic(G1, G2):
                break
        else:
            # or add it to unique list
            g_uniq.append(G1)
    # return list 
    return g_uniq

# Maximum number of edges (to permute)
m_max = n*(n-1)
# Rename nodes from 0-3 to A-D for topofiles
repl_d = {0:'A',1:'B',2:'C',3:'D'}
# Get a complete digraph
g_c = nx.complete_graph(m,nx.DiGraph())
# Convert it to topo file format with all inhibition
df_c = nx.to_pandas_edgelist(g_c)
df_c['type']=2
# Make directories
os.makedir('./figures_'+str(n)+'/')
os.makedir('./topfiles_'+str(n)+'/')
# Iterate over no. of permutations
for m in range(m_max+1):
    print(n)
    g_u = unique_graphs(m)
    # Number of unique networks
    print('nos',len(g_u))
    g_n=0
    for g in g_u:
        # Plot the graph and save it (not a clear visualization)
        nx.draw(g)

        plt.savefig('./figures_'+str(n)+'/'+str(m)+'_'+str(g_n)+'.svg')
        plt.clf()
        # Convert the Graph to dataframe
        df_g = nx.to_pandas_edgelist(g)
        df = df_c.copy()
        # ????
        keys = list(df_g.columns.values)
        i1 = df[keys].set_index(keys).index
        i2 = df_g.set_index(keys).index
        # Set the edge as activation if edge exists in df_g
        df.loc[i1.isin(i2),'type']=1
        # Rename nodes
        df[keys] = df[keys].replace(repl_d)
        # Save the topofile
        df.to_csv('./topfiles_'+str(n)+'/'+str(m)+'_'+str(g_n)+'.topo',sep='\t',index=False)
        g_n+=1
