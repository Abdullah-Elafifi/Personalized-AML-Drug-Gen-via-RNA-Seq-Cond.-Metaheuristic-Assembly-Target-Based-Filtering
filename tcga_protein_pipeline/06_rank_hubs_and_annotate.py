import pandas as pd
import numpy as np
import mygene
import json
from sklearn.preprocessing import minmax_scale

def rank_and_annotate(
    hvgs_file,
    intramod_file,
    modules_json,
    gene_expr_file,
    top_n=20,
    out_file="results/top20_biomarkers_annotated.csv",
    all_ranked_file="results/all_ranked_biomarkers.csv"
):
    # --- Load HVGs and intramodular connectivity ---
    hvgs = pd.read_csv(hvgs_file, index_col=0)
    k_within = pd.read_csv(intramod_file, index_col=0)

    if k_within.shape[1] == 1:
        k_within = k_within.iloc[:, 0]  # flatten to Series

    # --- Load modules.json safely ---
    try:
        with open(modules_json, "r") as f:
            modules = json.load(f)
        modules = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in modules.items()]))
    except Exception as e:
        print(f"️Warning: could not parse {modules_json}: {e}")
        modules = pd.DataFrame()

    # --- Expression stats ---
    expr = pd.read_csv(gene_expr_file, index_col=0)
    mean_expr = expr.mean(axis=1)
    var_expr = expr.var(axis=1)

    # --- Combine metrics ---
    genes = hvgs.index.intersection(expr.index)
    df = pd.DataFrame(index=genes)
    df["mean"] = mean_expr.reindex(df.index)
    df["variance"] = var_expr.reindex(df.index)
    df["kWithin"] = k_within.reindex(df.index).fillna(0.0)

    # --- Normalize metrics ---
    df["mean_s"] = minmax_scale(df["mean"].fillna(0))
    df["var_s"] = minmax_scale(df["variance"].fillna(0))
    df["k_s"] = minmax_scale(df["kWithin"].fillna(0))

    # --- Composite score ---
    df["score"] = 0.5 * df["k_s"] + 0.3 * df["var_s"] + 0.2 * df["mean_s"]
    df = df.sort_values("score", ascending=False)

    # --- Annotate top genes ---
    mg = mygene.MyGeneInfo()
    top = df.head(max(top_n, 200)).index.tolist()  # query extra
    try:
        query = mg.querymany(
            top, scopes="symbol",
            fields="type_of_gene,uniprot,entrezgene,go,alias",
            species="human", verbose=False
        )
    except Exception as e:
        print(f"MyGene query failed: {e}")
        query = []

    ann = {}
    for q in query:
        if "notfound" in q and q["notfound"]:
            continue
        name = q.get("query")

        # --- Normalize UniProt to accession (string) ---
        uni_raw = q.get("uniprot")
        accession = None
        if isinstance(uni_raw, dict):
            accession = uni_raw.get("Swiss-Prot") or uni_raw.get("TrEMBL")
            if isinstance(accession, list):
                accession = accession[0]
        elif isinstance(uni_raw, list):
            accession = uni_raw[0]
        elif isinstance(uni_raw, str):
            accession = uni_raw

        ann[name] = {
            "type_of_gene": q.get("type_of_gene"),
            "uniprot": uni_raw,
            "Entry": accession,  # 🔹 clean UniProt ID for AlphaFold
            "entrez": q.get("entrezgene"),
            "go": q.get("go"),
            "alias": q.get("alias")
        }

    ann_df = pd.DataFrame.from_dict(ann, orient="index")
    merged = df.merge(ann_df, left_index=True, right_index=True, how="left")

    # --- Targetability flag ---
    def flag_targetable(go):
        if not isinstance(go, dict):
            return ""
        cc = go.get("CC")
        terms = ""
        if isinstance(cc, list):
            terms = " ".join([t.get("term", "").lower() for t in cc if isinstance(t, dict)])
        elif isinstance(cc, dict):
            terms = cc.get("term", "").lower()
        if any(x in terms for x in ["membrane", "plasma membrane", "extracellular", "secreted"]):
            return "surface/secreted"
        return ""

    merged["targetability"] = merged["go"].apply(flag_targetable)

    # --- Save outputs ---
    final = merged.head(top_n)
    merged.to_csv(all_ranked_file)
    final.to_csv(out_file)

    print(f" Saved top {top_n} biomarkers → {out_file}")
    print(f" Full ranking saved → {all_ranked_file}")
    return final

if __name__ == "__main__":
    final = rank_and_annotate(
        "results/hvgs_2000.csv",
        "results/intramodular_connectivity.csv",
        "results/modules.json",
        "data/gene_expression_protein_coding.csv",
        top_n=20,
        out_file="results/top20_biomarkers_annotated.csv"
    )
    print(final[["score","kWithin","variance","mean","type_of_gene","Entry","targetability"]])
