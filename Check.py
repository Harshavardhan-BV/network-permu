import numpy as np
import pandas as pd
import networkx as nx
import glob
import networkx.algorithms.isomorphism as iso

# Folder One
folder1 = 'topofiles_3'
type1 = 'topo'
# Folder Two
folder2 = '3UniqueTOPOS'
type2 = 'adj'

def topo_to_G(topofiles):
    # Read all topofiles and convert to networkx graph
    topo_graphs = []
    for topo_file in topofiles:
        df = pd.read_csv(topo_file, sep='\t')
        df.columns = ['source', 'target', 'weight']
        G = nx.from_pandas_edgelist(df, 'source', 'target', edge_attr='weight', create_using=nx.DiGraph())
        topo_graphs.append(G)
    return topo_graphs

def adj_to_G(adjfiles, selfe=0):
    # Read all adjacency matrix and convert to networkx graph
    adj_graphs = []
    for adj_file in adjfiles:
        df = pd.read_csv(adj_file, index_col=0, dtype=int).values
        # Set diagonal to 0
        np.fill_diagonal(df, selfe)
        G = nx.from_numpy_array(df, create_using=nx.DiGraph)
        adj_graphs.append(G)
    return adj_graphs

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
    isograph = pd.DataFrame(isograph, columns=[folder1, folder2])
    isograph.to_csv(f'Isographs_{folder1}_{folder2}.csv', index=False)
    return isograph

graph_gen = {'topo': topo_to_G, 'adj': adj_to_G}
ext = {'topo': 'topo', 'adj': 'csv'}
files1 = glob.glob(f'{folder1}/*.{ext[type1]}')
files2 = glob.glob(f'{folder2}/*.{ext[type2]}')
graphs1 = graph_gen[type1](files1)
graphs2 = graph_gen[type2](files2)
isolol = isomorphic_graphs(graphs1, files1, graphs2, files2)
# Find files not in isographs
print(f'Files not from {folder1}')
print([x for x in files1 if x not in isolol[folder1].values])
print(f'Files not from {folder2}')
print([x for x in files2 if x not in isolol[folder2].values])
