from os import listdir
import networkx as nx
# import math
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt

dir_ = 'data/'
filenames = [filename for filename in listdir(dir_) if filename.endswith('.csv')]

leg = ["20%", "30%", "40%", "50%", "60%", "70%"]
closeness_centrality = []
full_set = None

for i in range(len(filenames)):
    file = filenames[i]
    
    # split into variables
    confidence, graphs, method, edgefunc = file.split('.')[0].split('_')
    confidence = confidence[10:]
    graphs = graphs[7:]
        
    if 'fiberlength' in file:
        df = pd.read_csv(dir_ + file, delimiter=';')
        df = df.rename(columns={'edge weight(med flm)':'weight'})
        df['len'] = df['weight']

        # generate digraph
        H = nx.from_pandas_edgelist(df, source='id node1', target='id node2',
                                    edge_attr=['weight','len'], create_using=nx.Graph())
        
        # remove self loops
        H.remove_edges_from(nx.selfloop_edges(H))
        
        # add nodes even though they have no edges (to make comparison more fair)
        if confidence == '20': full_set = set(H)
        else: H.add_nodes_from(full_set - set(H))
        
        # for centrality
        cc = nx.closeness_centrality(H)
        cc = {k:v for k,v in sorted(cc.items(), key=lambda s: s[0])}
        closeness_centrality.append(list(cc.values()))

cc_sort = pd.DataFrame({
    "20": closeness_centrality[0],
    "30": closeness_centrality[1],
    "40": closeness_centrality[2],
    "50": closeness_centrality[3],
    "60": closeness_centrality[4],
    "70": closeness_centrality[5]
}).sort_values(by="20")
cc_sort = cc_sort.reset_index(drop=True)

fig, axes = plt.subplots(figsize=(18,11), nrows=1, ncols=1)

for i in range(6):
    axes.scatter(cc_sort.index, cc_sort.iloc[:,i], s=5)

axes.grid(True)
axes.set_title("Closeness Centrality", fontdict={'fontsize': 20})
axes.set_xlabel('Node IDs', fontdict={'fontsize': 17})
axes.legend(leg)
plt.savefig('results/bosam3/test.png')