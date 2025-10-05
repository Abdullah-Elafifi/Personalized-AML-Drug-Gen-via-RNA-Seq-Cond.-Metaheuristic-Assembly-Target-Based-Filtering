import numpy as np
import pandas as pd

def normalize_log(expr):
    # assume expr is already RPKM/TPM-like; if raw counts you should use DESeq2 in R
    # We'll compute log2(x + 1)
    return np.log2(expr + 1.0)

def select_hvgs(expr_file, out_hvgs, n_hvgs=2000, min_mean=0.5):
    expr = pd.read_csv(expr_file, index_col=0)
    expr_norm = normalize_log(expr)

    # remove low mean expression genes
    mean_expr = expr_norm.mean(axis=1)
    expr_f = expr_norm.loc[mean_expr >= min_mean]
    print("After mean filter:", expr_f.shape)

    # compute variance (or dispersion)
    var = expr_f.var(axis=1)
    # optionally compute mean-variance relationship and compute scaled residuals; we'll use simple ranking
    hvgs = var.sort_values(ascending=False).head(n_hvgs)
    hvgs_df = expr_f.loc[hvgs.index]
    hvgs_df.to_csv(out_hvgs)
    # Save variance table
    pd.DataFrame({"mean": mean_expr.loc[hvgs.index], "variance": var.loc[hvgs.index]}).to_csv(out_hvgs.replace(".csv","_stats.csv"))
    print(f"Saved top {n_hvgs} HVGs to {out_hvgs}")

if __name__ == "__main__":
    select_hvgs("data/gene_expression_protein_coding.csv", "results/hvgs_2000.csv", n_hvgs=2000, min_mean=0.5)
