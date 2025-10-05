import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import json
import networkx as nx
from networkx.algorithms import community

def build_adjacency(expr_df, power=6):
    # expr_df: genes x samples (already normalized)
    corr = expr_df.T.corr()  # gene-gene Pearson correlation
    # soft threshold adjacency
    adj = corr.abs() ** power
    np.fill_diagonal(adj.values, 0.0)
    return adj

def module_detection(adj_matrix):
    # Use a greedy modularity communities detection on weighted graph
    G = nx.from_pandas_adjacency(adj_matrix)
    # convert to unweighted for greedy? greedy_modularity_communities accepts weighted but may treat weights variably.
    communities = list(community.greedy_modularity_communities(G, weight='weight'))
    modules = {f"module_{i+1}": list(c) for i,c in enumerate(communities)}
    return modules, G

def module_eigengenes(expr_df, modules):
    eig = {}
    for mname, genes in modules.items():
        if len(genes) < 2:
            eig[mname] = pd.Series([0]*expr_df.shape[1], index=expr_df.columns)
            continue
        # PCA on genes x samples -> take first PC
        pca = PCA(n_components=1)
        comp = pca.fit_transform(expr_df.loc[genes].T).flatten()
        eig[mname] = pd.Series(comp, index=expr_df.columns)
    eig_df = pd.DataFrame(eig)
    return eig_df

def intramodular_connectivity(adj, modules):
    # For each gene, sum adj weights to genes in same module
    k_within = {}
    for mname, genes in modules.items():
        sub = adj.loc[genes, genes]
        s = sub.sum(axis=1)
        for g in genes:
            k_within[g] = s.loc[g]
    return pd.Series(k_within)

if __name__ == "__main__":
    expr = pd.read_csv("results/hvgs_2000.csv", index_col=0)   # genes x samples
    print("HVG matrix shape:", expr.shape)

    adj = build_adjacency(expr, power=6)   # WGCNA-like soft threshold (beta=6)
    modules, G = module_detection(adj)
    print("Detected modules:", {k: len(v) for k,v in modules.items()})

    eig_df = module_eigengenes(expr, modules)
    eig_df.to_csv("results/module_eigengenes.csv")

    k_within = intramodular_connectivity(adj, modules)
    k_within.to_csv("results/intramodular_connectivity.csv", header=["kWithin"])

    # Save modules to json
    with open("results/modules.json","w") as f:
        json.dump(modules, f, indent=2)

    print("Saved modules, eigengenes, and intramodular connectivity.")
