# Import packages
import os
import itertools
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Number of nodes in graph
n=2 #(change here)

# Initialize empty n node graph
G = nx.DiGraph()
G.add_nodes_from(range(0,n))

# Get all possible graphs with m edges network
def get_possible_edges(m,p):
    # generate all possible pairs of nodes
    node_pairs = list(itertools.product(range(0, n), repeat=2))
    # create all possible permutations of n edges
    edge_permutations = list(itertools.combinations(node_pairs, m))
    # +ve edges
    p_edge_permutations = list(itertools.combinations(range(m),p))
    # create a list of graphs with each permutation of edges
    graphs = []
    for p_edge in p_edge_permutations:
        #change weights of edges
        weights = [1 if i in p_edge else 2 for i in range(0,m)]
        for edges in edge_permutations:
            G1 = G.copy()
            for i in range(len(edges)):
                G1.add_edge(edges[i][0],edges[i][1],weight=weights[i])
            graphs.append(G1)
    return graphs

# Select the unique graphs (ie do not repeat isomorphic ones)
def unique_graphs(m,p):
    # get all combinations with m edges
    gs = get_possible_edges(m,p)
    g_uniq=[]
    for G1 in gs:
        for G2 in g_uniq:
            # if the graph is isomorphic to existing do nothing
            if nx.algorithms.is_isomorphic(G1, G2, edge_match=nx.algorithms.isomorphism.numerical_edge_match('weight', 1)):
                break
        else:
            # or add it to unique list
            g_uniq.append(G1)
    # return list 
    return g_uniq

# Maximum number of edges (to permute)
m_max = n**2
# Rename nodes from 0-3 to A-D for topofiles
repl_d = {0:'A',1:'B',2:'C',3:'D'}
# Get a complete digraph
g_c = nx.complete_graph(n,nx.DiGraph())
# Convert it to topo file format with all inhibition
df_c = nx.to_pandas_edgelist(g_c)
df_c['type']=2
# Make directories
os.makedirs('./figures_'+str(n)+'/')
os.makedirs('./topofiles_'+str(n)+'/')
# Iterate over no. of permutations
for m in range(m_max+1):
    print('Edges',m)
    for p in range(0,m+1):
        print('Positive edges',p)
        g_u = unique_graphs(m,p)
        # Number of unique networks
        print('nos',len(g_u))
        g_n=0
        for g in g_u:
            # Plot the graph with edge color red if 1 and blue if 2
            nx.draw(g, edge_color=[ 'r' if g[u][v]['weight']==2 else 'b' for u,v in g.edges()])
            plt.savefig('./figures_'+str(n)+'/'+str(m)+'_'+str(p)+'_'+str(g_n)+'.svg')
            plt.clf()
            # Convert the Graph to dataframe
            df = nx.to_pandas_edgelist(g)
            # Rename nodes
            keys = ['source','target']
            df[keys] = df[keys].replace(repl_d)
            # Save the topofile
            df.to_csv('./topofiles_'+str(n)+'/'+str(m)+'_'+str(p)+'_'+str(g_n)+'.topo',sep='\t',index=False)
            g_n+=1
