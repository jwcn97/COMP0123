from os import listdir
import networkx as nx
import pandas as pd
import community
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout as layout

dir_ = 'data/'
filenames = [filename for filename in listdir(dir_) if filename.endswith('.csv')]
full_set = None
fdt = {'fontsize': 20}

def bosam(H, confidence):
    # sort nodes based on degree and max neighbor degree
    deg = {k:v for k,v in H.degree()}
    
    # find maximum degree of neighbors
    max_nb = []
    for key in deg:
        nb = [n for n in H.neighbors(key)]
        nb = [deg[i] for i in nb]
        nb = max(nb) if len(nb) > 0 else 0
        max_nb.append(nb)

    d1 = pd.DataFrame({
        'node': list(deg.keys()),
        'degree': list(deg.values()),
        'neighbor': max_nb
    })
    d1 = d1.sort_values(['degree', 'neighbor'])
    d1 = d1.reset_index(drop=True)
    
    # plot matrix
    A = nx.to_numpy_matrix(H, nodelist=d1['node'])
    fig = plt.figure(figsize=(14,14))
    plt.title("Power Law Model", fdt)
    ax = fig.add_subplot(111)
    ax.matshow(A, vmin=0, vmax=1)
    plt.savefig('results/network-graph/'+confidence+'.png')

def plot_communities(G, title_):
    pos = nx.spring_layout(G, weight='weight')
    partition = community.best_partition(G)  # compute communities that yields the highest modularity

    plt.figure(figsize=(16,10))
    plt.title("Confidence: " + title_ + " %", fdt)
    nx.draw_networkx_nodes(G, pos, node_size=60, cmap=plt.cm.RdYlBu, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    plt.box(on=None)
    plt.axis('off')
    # plt.savefig('results/bosam3/graphs-'+ title_ +'.png')

def plot_circular(G, title_):
    pos = nx.circular_layout(G, weight='weight')
    # pos = layout(G, prog="twopi", args="")
    plt.figure(figsize=(10, 10))
    plt.title("Confidence: " + title_ + " %", fdt)
    nx.draw(G, pos, node_size=10, linewidths=0.7, alpha=0.5, node_color="blue", with_labels=False)
    plt.axis("equal")
    plt.box(on=None)
    plt.axis('off')
    plt.savefig('results/bosam3/circulars-'+ title_ +'.png')

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

        # # get largest component in graph
        # Gc = max(nx.connected_component_subgraphs(H), key=len)
        
        # # add nodes even though they have no edges (to make comparison more fair)
        if confidence == '20': full_set = set(H)
        else: H.add_nodes_from(full_set - set(H))
            
        # bosam(H, confidence)
        # plot_communities(Gc, confidence)
        # plot_circular(Gc, confidence)
