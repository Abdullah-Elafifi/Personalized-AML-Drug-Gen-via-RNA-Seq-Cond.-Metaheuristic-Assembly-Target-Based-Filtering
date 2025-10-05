import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import umap.umap_ as umap
import networkx as nx

outdir = "results_for_biomarkers"
os.makedirs(outdir, exist_ok=True)

# Load protein-coding gene expression data
expr = pd.read_csv("data/gene_expression_protein_coding.csv", index_col=0)

# Select Top 20 Biomarkers
# Step 1: variance across samples
gene_var = expr.var(axis=1).sort_values(ascending=False)

# Step 2: filter out hemoglobins
filtered_genes = gene_var[~gene_var.index.str.contains("HB|globin", case=False, regex=True)]

# Step 3: take top 20 after filtering
top20 = filtered_genes.head(20)
top20_df = expr.loc[top20.index]

# Save biomarker data
top20_df.to_csv(f"{outdir}/top20_biomarkers.csv")
print("\nTop 20 biomarker genes (variance-based, hemoglobins excluded):")
print(top20)
print(f"\nSaved to: {outdir}/top20_biomarkers.csv")

# Statistics
summary_stats = top20_df.describe()
summary_stats.to_csv(f"{outdir}/top20_summary.csv")

# Expression distribution
plt.figure(figsize=(8,5))
sns.histplot(top20_df.values.flatten(), bins=50, kde=True)
plt.title("Expression Distribution (Top 20 Biomarkers)")
plt.savefig(f"{outdir}/top20_distribution.png")
plt.close()

# Heatmap (Top 20 biomarkers)
clust = sns.clustermap(
    top20_df,
    cmap="plasma",
    metric="correlation",
    method="average",
    standard_scale=1,
    figsize=(12, 8)
)
clust.fig.suptitle("Clustered Heatmap (Top 20 Biomarkers)", y=1.02)
clust.savefig(f"{outdir}/top20_heatmap.png")
plt.close()

# PCA (samples, top 20 biomarkers)
pca = PCA(n_components=2)
pca_res = pca.fit_transform(top20_df.T)
pca_df = pd.DataFrame(pca_res, columns=["PC1","PC2"])
pca_df.to_csv(f"{outdir}/top20_pca.csv")

plt.figure(figsize=(7,6))
sns.scatterplot(data=pca_df, x="PC1", y="PC2")
plt.title("PCA of Samples (Top 20 Biomarkers)")
plt.savefig(f"{outdir}/top20_pca.png")
plt.close()

# UMAP (samples, top 20 biomarkers)
reducer = umap.UMAP(random_state=42)
umap_res = reducer.fit_transform(top20_df.T)
umap_df = pd.DataFrame(umap_res, columns=["UMAP1","UMAP2"])
umap_df.to_csv(f"{outdir}/top20_umap.csv")

plt.figure(figsize=(7,6))
sns.scatterplot(data=umap_df, x="UMAP1", y="UMAP2")
plt.title("UMAP of Samples (Top 20 Biomarkers)")
plt.savefig(f"{outdir}/top20_umap.png")
plt.close()

# Gene Co-expression Network
corr = top20_df.T.corr()
G = nx.Graph()
for g1 in corr.columns:
    for g2 in corr.columns:
        if g1 < g2 and corr.loc[g1, g2] > 0.7:
            G.add_edge(g1, g2, weight=corr.loc[g1, g2])

plt.figure(figsize=(10,8))
nx.draw_networkx(G, node_size=300, font_size=8)
plt.title("Gene Co-expression Network (Top 20 Biomarkers)")
plt.savefig(f"{outdir}/top20_network.png")
plt.close()
