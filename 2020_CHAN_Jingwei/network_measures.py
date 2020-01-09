from os import listdir
import networkx as nx
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import powerlaw

dir_ = 'data/'
filenames = [filename for filename in listdir(dir_) if filename.endswith('.csv')]

fig, axes = plt.subplots(figsize=(18,45), nrows=6, ncols=1)
models = ["data","Powerlaw Model"]

leg = ["20%", "30%", "40%", "50%", "60%", "70%"]
clustering_m, tc_m, global_efficiency_m, assort_m = [], [], [], []
full_set = None
fdt = {'fontsize': 20}
fd = {'fontsize': 17}

def plot(G, ind, confidence):
    for H in G:
        in_degrees = H.degree()
        in_values = sorted(set([x[1] for x in in_degrees]))
        in_hist = [[x[1] for x in in_degrees].count(x) for x in in_values]

        axes[ind].loglog(in_values, in_hist, 'o-')
        
    axes[ind].set_title("Confidence: " + confidence + " %", fdt)
    axes[ind].set_ylabel("Occurences", fd)
    axes[ind].set_xlabel("Degree", fd)
    axes[ind].grid(True)
    axes[ind].set_xlim([0, 200])
    axes[ind].legend(models)

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
            
        N = H.order()
        
        s = nx.utils.powerlaw_sequence(N, ((float(confidence)+20)/20))
        M = [H]#, nx.expected_degree_graph(s, selfloops=False)]
        
        plot(M, i, confidence)
        
        # for functional segregation
        clustering_m.append([nx.average_clustering(g) for g in M])
        tc_m.append([nx.transitivity(g) for g in M])
        
        # for functional integration
        global_efficiency_m.append([nx.global_efficiency(g) for g in M])
        
        # for network resilience
        assort_m.append([nx.degree_assortativity_coefficient(g) for g in M])

####################################

fig, axe = plt.subplots(figsize=(18,14), nrows=2, ncols=2)

for i in range(len(clustering_m[0])):
    axe[0,0].plot(leg, [x[i] for x in clustering_m], 'o-')
    axe[0,1].plot(leg, [x[i] for x in tc_m], 'o-')
    axe[1,0].plot(leg, [x[i] for x in global_efficiency_m], 'o-')
    axe[1,1].plot(leg, [x[i] for x in assort_m], 'o-')

axe[0,0].set_title('Clustering Coefficient', fontdict=fdt)
axe[0,1].set_title('Transitivity', fontdict=fdt)
axe[1,0].set_title('Global Efficiency', fontdict=fdt)
axe[1,1].set_title('Assortative Coefficient', fontdict=fdt)

for i in range(len(axe)):
    for j in range(2):
        axe[i,j].grid(True)
        axe[i,j].set_xlabel('Confidence Level (%)', fontdict=fd)
        axe[i,j].legend(models)
        
plt.show()