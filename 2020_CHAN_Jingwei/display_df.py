from os import listdir
import networkx as nx
import pandas as pd

dir_ = 'data/'
filenames = [filename for filename in listdir(dir_) if filename.endswith('.csv')]
full_set = None

df1 = pd.DataFrame(columns=["confidence","edges","density","diameter","transitivity"])

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
        
        # get largest component in graph
        Gc = max(nx.connected_component_subgraphs(H), key=len)
        di = nx.diameter(Gc)

        # calculate stats
        d = nx.density(H)
        e = H.size()
        trans = nx.transitivity(H)
        
        df1 = df1.append({
            'confidence': confidence + "%",
            'edges': e,
            'density': round(d, 3),
            'diameter': di,
            'transitivity': round(trans, 3)
        }, ignore_index=True)
        
print(df1)