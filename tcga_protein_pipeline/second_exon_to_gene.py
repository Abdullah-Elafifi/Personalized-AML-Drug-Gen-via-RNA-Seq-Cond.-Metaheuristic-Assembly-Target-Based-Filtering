import pandas as pd

def map_exons_to_genes(expression_file, mapping_file, output_file):
    expr = pd.read_csv(expression_file, index_col=0)
    mapping = pd.read_csv(mapping_file, sep="\t")[["id", "gene"]].dropna().drop_duplicates()
    mapping = mapping.rename(columns={"id": "exon"}).set_index("exon")

    expr = expr.loc[expr.index.intersection(mapping.index)]
    expr["gene"] = mapping.loc[expr.index, "gene"]

    gene_expr = expr.groupby("gene").mean()
    gene_expr.to_csv(output_file)

    print("Gene-level expression saved to:", output_file)
    print("Final shape:", gene_expr.shape)

if __name__ == "__main__":
    map_exons_to_genes("data/expression_clean.csv",
                       "data/unc_v2_exon_hg19_probe_TCGA",
                       "data/gene_expression.csv")
