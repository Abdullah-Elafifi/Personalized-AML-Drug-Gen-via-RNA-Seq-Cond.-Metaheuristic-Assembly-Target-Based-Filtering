import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import umap.umap_ as umap
import networkx as nx
from scipy.cluster.hierarchy import linkage, dendrogram
from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor, DistanceMatrix
from sklearn.metrics import silhouette_score

# ----------------------------
# Setup
# ----------------------------
os.makedirs("results", exist_ok=True)

# Load data
expr = pd.read_csv("data/gene_expression.csv", index_col=0)

# ----------------------------
# Basic Statistics
# ----------------------------
summary_stats = expr.describe()
summary_stats.to_csv("results/expression_summary.csv")

gene_var = expr.var(axis=1).sort_values(ascending=False)
gene_var.to_csv("results/gene_variance.csv")

top_genes = expr.mean(axis=1).sort_values(ascending=False).head(50)
top_genes.to_csv("results/top_genes.csv")

# Distribution
plt.figure(figsize=(8,5))
sns.histplot(expr.values.flatten(), bins=100, kde=True)
plt.title("Distribution of Expression Values")
plt.savefig("results/expression_distribution.png")
plt.close()

# Heatmap of top genes
plt.figure(figsize=(12, 10))
clust = sns.clustermap(
    expr.loc[top_genes.index],
    cmap="viridis",
    metric="correlation",   # distance metric for clustering
    method="average",       # linkage method
    standard_scale=1,       # normalize per gene across samples
    figsize=(12, 10)
)
clust.fig.suptitle("Clustered Heatmap of Top 50 Highly Expressed Genes", y=1.02)
clust.savefig("results/top50_clustered_heatmap.png")
plt.close()

# ----------------------------
# PCA
# ----------------------------

pca = PCA(n_components=2)
pca_res = pca.fit_transform(expr.T)
pca_df = pd.DataFrame(pca_res, columns=["PC1","PC2"])
pca_df.to_csv("results/pca_coordinates.csv")

# ----------------------------
# Determine best number of clusters using ((((((silhouette score)))
# ----------------------------
scores = []
K = range(2, 10)  # try 2 to 9 clusters
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42).fit(expr.T)
    labels = kmeans.labels_
    score = silhouette_score(expr.T, labels)
    scores.append(score)

best_k = K[scores.index(max(scores))]
print("Best number of clusters based on silhouette score:", best_k)

# ----------------------------
# Cluster with the best k
# ----------------------------
kmeans = KMeans(n_clusters=best_k, random_state=42).fit(expr.T)
pca_df["Cluster"] = kmeans.labels_.astype(str)

# ----------------------------
# Plot PCA colored by clusters
# ----------------------------
plt.figure(figsize=(7,6))
sns.scatterplot(
    data=pca_df,
    x="PC1",
    y="PC2",
    hue="Cluster",       # color by cluster
    palette="tab10",
    s=80
)
plt.title(f"PCA of Samples (k={best_k} clusters)")
plt.legend(title="Cluster")
plt.tight_layout()
plt.savefig("results/pca_plot_clusters.png")
plt.close()

# ----------------------------
# UMAP
# ----------------------------
reducer = umap.UMAP(random_state=42)
umap_res = reducer.fit_transform(expr.T)
umap_df = pd.DataFrame(umap_res, columns=["UMAP1","UMAP2"])

# Unsupervised clustering (e.g., 2 clusters)
kmeans = KMeans(n_clusters=2, random_state=42).fit(expr.T)
umap_df["Cluster"] = kmeans.labels_.astype(str)

# Plot
plt.figure(figsize=(7,6))
sns.scatterplot(
    data=umap_df,
    x="UMAP1",
    y="UMAP2",
    hue="Cluster",        # color by cluster
    palette="tab10",
    s=80
)
# ----------------------------
# MA Plot
# ----------------------------
def plot_ma(df, cond1, cond2, outfile):
    mean_expr = df[[cond1, cond2]].mean(axis=1)
    log_fc = np.log2(df[cond1] + 1) - np.log2(df[cond2] + 1)
    plt.figure(figsize=(8,6))
    plt.scatter(mean_expr, log_fc, alpha=0.5)
    plt.axhline(0, color="red", linestyle="--")
    plt.xlabel("Mean Expression")
    plt.ylabel("Log2 Fold Change")
    plt.title(f"MA Plot: {cond1} vs {cond2}")
    plt.savefig(outfile)
    plt.close()

if expr.shape[1] >= 2:
    samples = expr.columns[:2]
    plot_ma(expr, samples[0], samples[1], "results/ma_plot.png")

# ----------------------------
# Gene Co-expression Network
# ----------------------------
corr = expr.corr()  # gene correlation
G = nx.Graph()
for g1 in corr.columns:
    for g2 in corr.columns:
        if g1 < g2 and corr.loc[g1,g2] > 0.9:
            G.add_edge(g1, g2, weight=corr.loc[g1,g2])

plt.figure(figsize=(10,8))
nx.draw_networkx(G, node_size=30, with_labels=False)
plt.title("Gene Co-expression Network")
plt.savefig("results/gene_network.png")
plt.close()
