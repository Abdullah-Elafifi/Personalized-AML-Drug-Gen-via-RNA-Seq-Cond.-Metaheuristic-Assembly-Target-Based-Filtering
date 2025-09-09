import pandas as pd

def map_exons_to_genes(expression_file, mapping_file, output_file):
    # Load expression data (cleaned exon-level expression)
    expr = pd.read_csv(expression_file, index_col=0)
    print("Expression shape before mapping:", expr.shape)

    # Load exon → gene mapping
    mapping = pd.read_csv(mapping_file, sep="\t")
    print("Mapping shape:", mapping.shape)
    print("Mapping columns:", mapping.columns.tolist())

    # Fix: rename 'id' to 'exon' to match expression index
    mapping = mapping[["id", "gene"]].dropna().drop_duplicates()
    mapping = mapping.rename(columns={"id": "exon"})
    mapping = mapping.set_index("exon")

    # Align expression data with mapping
    expr = expr.loc[expr.index.intersection(mapping.index)]

    # Add gene symbols
    expr["gene"] = mapping.loc[expr.index, "gene"]

    # Group by gene (aggregate across exons)
    gene_expr = expr.groupby("gene").mean()

    # Save result
    gene_expr.to_csv(output_file)
    print("Gene-level expression saved to:", output_file)
    print("Final shape:", gene_expr.shape)

if __name__ == "__main__":
    map_exons_to_genes(
        "data/expression_clean.csv",
        "data/unc_v2_exon_hg19_probe_TCGA",
        "data/gene_expression.csv"
    )