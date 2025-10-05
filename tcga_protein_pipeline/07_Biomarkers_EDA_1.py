import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import networkx as nx
import umap.umap_ as umap
from scipy.cluster.hierarchy import linkage, dendrogram

os.makedirs("Biomarkers_results_graphs", exist_ok=True)

expr = pd.read_csv("data/gene_expression.csv", index_col=0)  # full matrix
biomarkers = pd.read_csv("results/top20_biomarkers_annotated.csv", index_col=0)
genes = biomarkers.index.tolist()

# 1. Heatmap of Top 20 Biomarkers
sns.clustermap(
    expr.loc[genes],
    cmap="RdBu_r",
    z_score=0,
    metric="correlation",
    method="average",
    figsize=(12, 8),
    xticklabels=False
)
plt.title("Top 20 Biomarkers Heatmap", y=1.02)
plt.savefig("Biomarkers_results_graphs/top20_biomarkers_heatmap.png")
plt.close()

# 2. PCA using Top Biomarkers
pca = PCA(n_components=2)
scaled = StandardScaler().fit_transform(expr.loc[genes].T)
pca_res = pca.fit_transform(scaled)
pca_df = pd.DataFrame(pca_res, columns=["PC1","PC2"], index=expr.columns)

plt.figure(figsize=(7,6))
sns.scatterplot(x="PC1", y="PC2", data=pca_df, s=80)
plt.title("PCA using Top 20 Biomarkers")
plt.savefig("Biomarkers_results_graphs/top20_pca.png")
plt.close()

# 3. Correlation Heatmap
corr = expr.loc[genes].T.corr()
plt.figure(figsize=(10,8))
sns.heatmap(corr, cmap="coolwarm", center=0, annot=True, fmt=".2f")
plt.title("Correlation Among Top 20 Biomarkers")
plt.savefig("Biomarkers_results_graphs/top20_correlation_heatmap.png")
plt.close()

# 4. Biomarker Network
G = nx.Graph()
for g1 in corr.columns:
    for g2 in corr.columns:
        if g1 < g2 and corr.loc[g1,g2] > 0.7:
            G.add_edge(g1, g2, weight=corr.loc[g1,g2])

plt.figure(figsize=(8,6))
nx.draw_networkx(G, with_labels=True, node_size=800, node_color="skyblue")
plt.title("Top 20 Biomarker Network (Corr > 0.7)")
plt.savefig("Biomarkers_results_graphs/top20_biomarker_network.png")
plt.close()

# 5. Volcano Plot (if available)
if "log2FC" in biomarkers.columns and "adj_pval" in biomarkers.columns:
    plt.figure(figsize=(8,6))
    plt.scatter(biomarkers["log2FC"], -np.log10(biomarkers["adj_pval"]), alpha=0.7)

    # highlight top 5
    top_hits = biomarkers.sort_values("adj_pval").head(5)
    plt.scatter(top_hits["log2FC"], -np.log10(top_hits["adj_pval"]), color="red")
    for i, row in top_hits.iterrows():
        plt.text(row["log2FC"], -np.log10(row["adj_pval"]), i)

    plt.axvline(0, color="grey", linestyle="--")
    plt.xlabel("Log2 Fold Change")
    plt.ylabel("-log10 Adjusted p-value")
    plt.title("Volcano Plot of Biomarker Candidates")
    plt.savefig("Biomarkers_results_graphs/top20_volcano.png")
    plt.close()

# 6. Boxplots of Biomarker Expression
plt.figure(figsize=(14,6))
expr.loc[genes].T.boxplot(rot=90)
plt.ylabel("Expression")
plt.title("Boxplots of Top 20 Biomarkers Across Samples")
plt.tight_layout()
plt.savefig("Biomarkers_results_graphs/top20_boxplots.png")
plt.close()

# 7. Violin plots
plt.figure(figsize=(14,6))
sns.violinplot(data=expr.loc[genes].T)
plt.xticks(rotation=90)
plt.ylabel("Expression")
plt.title("Violin Plots of Top 20 Biomarkers")
plt.tight_layout()
plt.savefig("Biomarkers_results_graphs/top20_violins.png")
plt.close()

# 8. Pairplot (scatter matrix)
sns.pairplot(expr.loc[genes].T.iloc[:, :6])  # first 6 biomarkers to avoid clutter
plt.savefig("Biomarkers_results_graphs/top20_pairplot.png")
plt.close()

# 9. Hierarchical Dendrogram (Samples)
Z = linkage(expr.loc[genes].T, method="average", metric="euclidean")
plt.figure(figsize=(10,6))
dendrogram(Z, labels=expr.columns, leaf_rotation=90)
plt.title("Hierarchical Clustering of Samples (Top 20 Biomarkers)")
plt.tight_layout()
plt.savefig("Biomarkers_results_graphs/top20_dendrogram.png")
plt.close()

# 10. UMAP Projection
reducer = umap.UMAP(random_state=42)
umap_res = reducer.fit_transform(expr.loc[genes].T)
umap_df = pd.DataFrame(umap_res, columns=["UMAP1","UMAP2"], index=expr.columns)

plt.figure(figsize=(7,6))
sns.scatterplot(x="UMAP1", y="UMAP2", data=umap_df, s=80)
plt.title("UMAP of Samples (Top 20 Biomarkers)")
plt.savefig("Biomarkers_results_graphs/top20_umap.png")
plt.close()

print("All advanced biomarker plots generated in Biomarkers_results_graphs/")
