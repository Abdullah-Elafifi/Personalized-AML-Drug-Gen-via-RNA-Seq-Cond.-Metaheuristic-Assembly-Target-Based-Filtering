"""
this is the linking pipline , enjoy....
"""
from first_load_data import *
from second_exon_to_gene import *
from third_filter_protein_coding import *
from fourth_normalize_and_select_hvgs import *


if __name__ == "__main__":
    expr = load_expression("data/TCGA.LAML.sampleMap_HiSeqV2_exon.gz")
    mapping = load_mapping("data/unc_v2_exon_hg19_probe_TCGA")
    
    with open("loging_pipline_data", "a") as f:
        f.write("first_file_pip_is_added.\n")
        print("Expression shape:", expr.shape,file=f)
        print("Mapping shape:", mapping.shape,file=f)

    gene_expr=map_exons_to_genes(expr,mapping,"gene_expr_file_from_the_second_function.csv")   
    with open("loging_pipline_data", "a") as f:
        f.write("second_file_pip_is_added.\n")
        print("gene_expr_file_is",gene_expr)
    
    dataNDgene_expression_protein_coding=filter_protein_coding(gene_expr,"data/gene_expression_protein_coding.csv")
    with open("loging_pipline_data", "a") as f:
        f.write("third_file_pip_is_added.\n")
        print("dataaNDgene_expression_protein_coding is : ",dataNDgene_expression_protein_coding)

    results_and_hvgs_2000=select_hvgs(dataNDgene_expression_protein_coding,"results/hvgs_2000.csv")
    with open("loging_pipline_data", "a") as f:
        f.write("fourth_file_pip_is_added.\n")
        print("results_and_hvgs_2000 is : ",results_and_hvgs_2000,"\n")


