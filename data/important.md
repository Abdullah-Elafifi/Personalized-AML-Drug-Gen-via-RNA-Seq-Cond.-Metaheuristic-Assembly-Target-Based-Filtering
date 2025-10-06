# Dataset Description

## **Dataset Title**
**TCGA Acute Myeloid Leukemia (LAML) – Exon Expression by RNAseq (polyA+ IlluminaHiSeq)**

---

## **Data Source**
- **Hub:** [https://tcga.xenahubs.net](https://tcga.xenahubs.net)  
- **Dataset Page:** [TCGA LAML Exon Expression (IlluminaHiSeq)](https://xenabrowser.net/datapages/?dataset=TCGA.LAML.sampleMap%2FHiSeqV2_exon&host=https%3A%2F%2Ftcga.xenahubs.net&removeHub=https%3A%2F%2Fxena.treehouse.gi.ucsc.edu%3A443)  
- **Provider:** The Cancer Genome Atlas (TCGA) via **UCSC Xena Browser**

---

## **Experimental Methodology**
The dataset represents **exon-level expression profiles** for **Acute Myeloid Leukemia (LAML)** samples.  
It was experimentally measured using the **Illumina HiSeq 2000 RNA Sequencing platform** by the **University of North Carolina TCGA Genome Characterization Center**.

- **RNA Source:** PolyA+ mRNA (enriched for mature messenger RNA)  
- **Platform:** Xenabrowser
- **Data Type:** Exon-level transcription estimates  
- **Units:** **RPKM** (Reads Per Kilobase of exon model per Million mapped reads)  
- **Processing Level:** **Level 3** TCGA data (processed and normalized)

---

## **Data Mapping & Normalization**
- Exons are mapped to the **human genome coordinates** using the **UCSC Xena `unc_RNAseq_exon` probeMap**.  
- Each exon’s expression value is reported as **RPKM**, allowing for cross-sample comparisons.  
- For visualization purposes, each gene or exon is **centered to zero** by subtracting its mean expression across samples — this highlights **differential expression patterns** between samples.  
- Users can view the **original (non-normalized)** values by adjusting the visualization settings within the UCSC Xena interface.

---

## **Reference & Documentation**
- **Institution:** University of North Carolina TCGA Genome Characterization Center  
- **Data Coordination:** TCGA Data Coordination Center (DCC)  
- **Method Reference:** See the DCC description linked on the dataset’s UCSC Xena page for details on experimental design and data preprocessing.

---

## **Usage in This Project**
This dataset serves as the **transcriptomic foundation** for:
- **Feature extraction and conditioning** in the *Personalized De Novo AML Drug Generation* pipeline.  
- **Differential exon expression analysis** to identify patient-specific molecular signatures.  
- **Integration with diffusion-based drug generation models** for **transcriptome-conditioned de novo molecule synthesis**.

---

## **Citation**
> The Cancer Genome Atlas (TCGA) Research Network. *Acute Myeloid Leukemia (LAML) RNAseq Exon Expression Data (IlluminaHiSeq)*.  
> University of North Carolina TCGA Genome Characterization Center.  
> Available at: [https://xenabrowser.net/datapages/?dataset=TCGA.LAML.sampleMap%2FHiSeqV2_exon&host=https%3A%2F%2Ftcga.xenahubs.net](https://xenabrowser.net/datapages/?dataset=TCGA.LAML.sampleMap%2FHiSeqV2_exon&host=https%3A%2F%2Ftcga.xenahubs.net)
