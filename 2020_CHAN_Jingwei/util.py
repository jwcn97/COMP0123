import networkx as nx
import numpy as np
import math
import matplotlib.pyplot as plt
import collections
import community
from networkx.drawing.nx_pydot import graphviz_layout as layout
from sklearn import cluster

def cal_nodesize(G):
    info = nx.info(G).split('\n')
    return int(info[2].strip().split(':')[1])

def plot_network(G, title_):
    plt.figure(figsize=(12,9))
    plt.title(title_)
    edges = G.edges()
    weights = [G[u][v]['weight'] for u,v in edges]
    nx.draw(G, node_size=60, node_color=range(cal_nodesize(G)), cmap=plt.cm.Blues, width=weights)
    # nx.draw(G, node_size=60, node_color=range(cal_nodesize(G)), cmap=plt.cm.Blues) 
    plt.show()
    
def plot_communities(G, title_):
    pos = nx.spring_layout(G)
    partition = community.best_partition(G)  # compute communities

    plt.figure(figsize=(16,10))
    plt.title(title_)
    nx.draw_networkx_nodes(G, pos, node_size=60, cmap=plt.cm.RdYlBu, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    plt.show()

def plot_circular(G, title_):
    pos = layout(G, prog="twopi", args="")
    plt.figure(figsize=(10, 10))
    plt.title(title_)
    nx.draw(G, pos, node_size=cal_nodesize(G), alpha=0.5, node_color="blue", with_labels=False)
    plt.axis("equal")
    plt.show()

def plot_hist(G, title_):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots(figsize=(14,7))
    plt.bar(deg, cnt, width=0.80, color="b")

    plt.title(title_)
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
    plt.show()
    
def plot_distribution_undirected(H, title_):
    in_degrees = H.degree() # dictionary node:degree
    in_values = sorted(set([x[1] for x in in_degrees]))
    in_hist = [[x[1] for x in in_degrees].count(x) for x in in_values]

    plt.figure(figsize=(16,6)) # you need to first do 'import pylab as plt'
    plt.grid(True)
    plt.loglog(in_values, in_hist, 'bv-') # in-degree
    plt.xlabel('Degree')
    plt.ylabel('Number of nodes')
    plt.title(title_)
    plt.xlim([0, 2*10**2])
    plt.show()
    
def plot_distribution(H, title_):
    in_degrees = H.in_degree() # dictionary node:degree
    in_values = sorted(set([x[1] for x in in_degrees]))
    in_hist = [[x[1] for x in in_degrees].count(x) for x in in_values]

    out_degrees = H.out_degree() # dictionary node:degree
    out_values = sorted(set([x[1] for x in out_degrees]))
    out_hist = [[x[1] for x in out_degrees].count(x) for x in out_values]

    plt.figure(figsize=(16,6)) # you need to first do 'import pylab as plt'
    plt.grid(True)
    plt.loglog(in_values, in_hist, 'ro-') # in-degree
    plt.loglog(out_values, out_hist, 'bv-') # out-degree
    plt.legend(['In-degree', 'Out-degree'])
    plt.xlabel('Degree')
    plt.ylabel('Number of nodes')
    plt.title(title_)
    plt.xlim([0, 2*10**2])
    plt.show()
    
def stats(G):
    # only works with digraph
    N, K = G.order(), G.size()
    avg_deg = float(K) / N
    print("Nodes: ", N)
    print("Edges: ", K)
    print("Average degree: ", avg_deg)
    print("SCC: ", nx.number_strongly_connected_components(G))
    print("WCC: ", nx.number_weakly_connected_components(G))
    
def plot_matrix(G, title_):
    A = nx.to_numpy_matrix(G)
    fig = plt.figure(figsize=(14,14))
    plt.title(title_)
    ax = fig.add_subplot(111)
    cax = ax.matshow(A)
    fig.colorbar(cax)
    
def plot_ordered_matrix(a, clusters, title_):
    model = cluster.AgglomerativeClustering(n_clusters=clusters,affinity="euclidean").fit(a)
    new_order = np.argsort(model.labels_)
    ordered_dist = a[new_order]
    ordered_dist = ordered_dist[:,new_order]

    fig = plt.figure(figsize=(14,14))
    plt.title(title_)
    ax = fig.add_subplot(111)
    cax = ax.matshow(ordered_dist)
    fig.colorbar(cax)