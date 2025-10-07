import pandas as pd
import mygene

def filter_protein_coding(input_file, output_file):
    mg = mygene.MyGeneInfo()
    gene_expr = pd.read_csv(input_file, index_col=0)

    query = mg.querymany(gene_expr.index.tolist(), scopes="symbol", fields="type_of_gene", species="human")
    gene_types = {q['query']: q.get('type_of_gene', None) for q in query}

    keep_genes = [g for g, t in gene_types.items() if t == "protein-coding"]
    filtered = gene_expr.loc[gene_expr.index.intersection(keep_genes)]
    filtered.to_csv(output_file)

    print(f"Filtered {gene_expr.shape[0]} → {filtered.shape[0]} (protein-coding only)")

if __name__ == "__main__":
    filter_protein_coding("data/gene_expression.csv", "data/gene_expression_protein_coding.csv")
