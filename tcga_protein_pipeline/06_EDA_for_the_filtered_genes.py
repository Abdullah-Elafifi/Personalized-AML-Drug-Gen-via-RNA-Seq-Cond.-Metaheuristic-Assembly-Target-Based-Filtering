import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import umap.umap_ as umap
import networkx as nx
from scipy.cluster.hierarchy import linkage, dendrogram

# ----------------------------
# Setup
# ----------------------------
outdir = "results_for_filtered_genes"
os.makedirs(outdir, exist_ok=True)

# Load protein-coding gene expression data
expr = pd.read_csv("data/gene_expression_protein_coding.csv", index_col=0)

# ----------------------------
# Top 20 Targets (variance-based, excluding hemoglobins)
# ----------------------------
gene_var = expr.var(axis=1).sort_values(ascending=False)

# Exclude hemoglobins (genes starting with "HB" or containing "globin")
filtered_genes = gene_var[~gene_var.index.str.contains("HB|globin", case=False, regex=True)]

# Select top 20 after filtering
top20 = filtered_genes.head(20)
top20_df = expr.loc[top20.index]

# Save CSV
top20_df.to_csv(f"{outdir}/top20_targets.csv")

# Print to console
print("\nTop 20 genes (by variance, hemoglobins excluded):")
print(top20)
print(f"\nTop 20 saved to: {outdir}/top20_targets.csv")

# ----------------------------
# Basic Statistics (top 20 only)
# ----------------------------
summary_stats = top20_df.describe()
summary_stats.to_csv(f"{outdir}/top20_expression_summary.csv")

# Distribution
plt.figure(figsize=(8,5))
sns.histplot(top20_df.values.flatten(), bins=50, kde=True)
plt.title("Distribution of Expression Values (Top 20 Genes, no Hemoglobins)")
plt.savefig(f"{outdir}/top20_distribution.png")
plt.close()

# Heatmap of top 20
clust = sns.clustermap(
    top20_df,
    cmap="plasma",
    metric="correlation",   # cluster by expression similarity
    method="average",       # linkage method
    standard_scale=1,       # normalize per gene across samples
    figsize=(12, 8)
)
clust.fig.suptitle("Clustered Heatmap of Top 20 Most Variable Protein-Coding Genes (No Hemoglobins)", y=1.02)
clust.savefig(f"{outdir}/top20_clustered_heatmap.png")
plt.close()

# ----------------------------
# PCA (samples using top 20 genes)
# ----------------------------
pca = PCA(n_components=2)
pca_res = pca.fit_transform(top20_df.T)
pca_df = pd.DataFrame(pca_res, columns=["PC1","PC2"])
pca_df.to_csv(f"{outdir}/top20_pca_coordinates.csv")

plt.figure(figsize=(7,6))
sns.scatterplot(data=pca_df, x="PC1", y="PC2")
plt.title("PCA of Samples (Top 20 Genes, no Hemoglobins)")
plt.savefig(f"{outdir}/top20_pca_plot.png")
plt.close()

# ----------------------------
# UMAP (samples using top 20 genes)
# ----------------------------
reducer = umap.UMAP()
umap_res = reducer.fit_transform(top20_df.T)
umap_df = pd.DataFrame(umap_res, columns=["UMAP1","UMAP2"])
umap_df.to_csv(f"{outdir}/top20_umap_coordinates.csv")

plt.figure(figsize=(7,6))
sns.scatterplot(data=umap_df, x="UMAP1", y="UMAP2")
plt.title("UMAP of Samples (Top 20 Genes, no Hemoglobins)")
plt.savefig(f"{outdir}/top20_umap_plot.png")
plt.close()

# ----------------------------
# Gene Co-expression Network (Top 20 only)
# ----------------------------
corr = top20_df.T.corr()
G = nx.Graph()
for g1 in corr.columns:
    for g2 in corr.columns:
        if g1 < g2 and corr.loc[g1,g2] > 0.7:  # lower threshold since only 20 genes
            G.add_edge(g1, g2, weight=corr.loc[g1,g2])

plt.figure(figsize=(10,8))
nx.draw_networkx(G, node_size=300, font_size=8)
plt.title("Gene Co-expression Network (Top 20 Genes, no Hemoglobins)")
plt.savefig(f"{outdir}/top20_gene_network.png")
plt.close()
