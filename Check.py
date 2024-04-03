#%%
import numpy as np
import pandas as pd
import networkx as nx
import glob
import networkx.algorithms.isomorphism as iso
#%%
# List all topofiles
topo_files = glob.glob('topofiles_3/*.topo')
# List all adjacency matrix files
adj_files = glob.glob('3UniqueTOPOS/*.csv')
#%%
def topo_to_G(topofiles):
    # Read all topofiles and convert to networkx graph
    topo_graphs = []
    for topo_file in topo_files:
        df = pd.read_csv(topo_file, sep='\t')
        df.columns = ['source', 'target', 'weight']
        G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='weight', create_using=nx.DiGraph())
        topo_graphs.append(G)
    return topo_graphs
#%%
topo_graphs = topo_to_G(topo_files)
#%%
def adj_to_G(adjfiles, selfe=0):
    # Read all adjacency matrix and convert to networkx graph
    adj_graphs = []
    for adj_file in adj_files:
        df = pd.read_csv(adj_file, index_col=0, dtype=int).values
        # Set diagonal to 0
        np.fill_diagonal(df, selfe)
        G = nx.from_numpy_array(df, create_using=nx.DiGraph)
        adj_graphs.append(G)
    return adj_graphs
#%%
adj_graphs = adj_to_G(adj_files)
# %%
def isomorphic_graphs(x_graphs, x_files, y_graphs, y_files):
    isograph = []
    em = iso.numerical_edge_match("weight", 0)
    # Check if any two graphs in x is isomorphic to each other
    for i in range(len(x_graphs)):
        for j in range(i+1, len(x_graphs)):
            if nx.is_isomorphic(x_graphs[i], x_graphs[j], edge_match=em):
                isograph.append([x_files[i], x_files[j]])
    # Check if any two graphs in y is isomorphic to each other
    for i in range(len(y_graphs)):
        for j in range(i+1, len(y_graphs)):
            if nx.is_isomorphic(y_graphs[i], y_graphs[j], edge_match=em):
                isograph.append([y_files[i], y_files[j]])
    # Check if any graph in x is isomorphic to any graph in y
    for i in range(len(x_graphs)):
        for j in range(len(y_graphs)):
            if nx.is_isomorphic(x_graphs[i], y_graphs[j], edge_match=em):
                isograph.append([x_files[i], y_files[j]])
    isograph = pd.DataFrame(isograph)
    isograph.to_csv('Isographs.csv')
    return isograph

# %%
isolol = isomorphic_graphs(topo_graphs, topo_files, adj_graphs, adj_files)
# %%
# Find files not in isographs
print([x for x in topo_files if x not in isolol[0].values])
print([x for x in adj_files if x not in isolol[1].values])
# %%
