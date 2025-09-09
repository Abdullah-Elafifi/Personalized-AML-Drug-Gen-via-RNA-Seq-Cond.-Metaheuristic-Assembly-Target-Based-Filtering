import pandas as pd

def load_expression(file_path):
    return pd.read_csv(file_path, sep="\t", index_col=0)

def load_mapping(file_path):
    return pd.read_csv(file_path, sep="\t")

if __name__ == "__main__":
    expr = load_expression("data/TCGA.LAML.sampleMap_HiSeqV2_exon.gz")
    mapping = load_mapping("data/unc_v2_exon_hg19_probe_TCGA")
    print("Expression shape:", expr.shape)
    print("Mapping shape:", mapping.shape)
