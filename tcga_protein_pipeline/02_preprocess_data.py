import pandas as pd

def preprocess_expression(df):
    df = df.dropna()                      # remove missing values
    df = df.loc[~df.index.duplicated()]   # remove duplicate exons
    return df

if __name__ == "__main__":
    expr = pd.read_csv("data/TCGA.LAML.sampleMap_HiSeqV2_exon.gz", sep="\t", index_col=0)
    expr_clean = preprocess_expression(expr)
    expr_clean.to_csv("data/expression_clean.csv")
    print("Preprocessed shape:", expr_clean.shape)
