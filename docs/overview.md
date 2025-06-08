# Project Overview

## Title
**Personalized De Novo Anti-Acute Leukaemia Drug Generation via Transcriptome-Conditioned Diffusion Models and Target-Driven Filtering**

## Institution
<b>Cairo University – Faculty of Computers and Artificial Intelligence</b>  
Department of Operations Research and Decision Support  

**Supervisor:** Prof. Tarek H. M. Aboulenien

## Team Members

- **Abdullah Elafifi** 
- **Youssef Khaled** 
- **Mariam Hanafy** 
- **Mohammed Alaa** 
- **Basma Mamduh** 

---

## Abstract
Acute Myeloid Leukemia (AML) is a genetically heterogeneous blood cancer with high relapse rates and limited precision therapies. This project proposes 
a deep learning pipeline that generates novel drug-like molecules tailored to individual AML patients based on their transcriptomic (RNA-Seq) profiles. 
Utilizing conditional diffusion models, the system synthesizes compounds conditioned on patient-specific gene expression embeddings. Candidate molecules 
are further filtered using predicted activity against AML-relevant targets, drug-likeness scores (e.g., QED), ADMET properties, and structural novelty.

The final pipeline is deployed as an interactive web application with open-source access, enabling end-to-end personalized drug discovery.

**Status:** Not completed – currently under development.

---

## Objectives
**Status:** Not completed – will be detailed progressively.

- Generate novel molecules conditioned on AML patient RNA-Seq profiles.  
- Ensure therapeutic relevance through target-based activity filtering (e.g., FLT3, IDH1, BCL2).  
- Apply ADMET prediction and drug-likeness scoring.  
- Use molecular docking to validate binding affinities.  
- Deploy a web interface for clinical or research usability.  
- Open-source the entire pipeline for reproducibility and community contribution.

---

## Key Technologies
**Status:** Not completed – technology stack to be finalized.

- **Machine Learning:** Conditional Latent Diffusion Models, Chemprop, XGBoost  
- **Bioinformatics:** RNA-Seq preprocessing, dimensionality reduction (PCA)  
- **Cheminformatics:** SMILES encoding, QED, ADMET filtering, Tanimoto similarity  
- **Molecular Docking:** 
- **Web Deployment:** 

---

## Project Management Approach: Agile Scrumban

We adopt an **Agile Scrumban** methodology to combine the structured iterative planning of Scrum with the continuous flow and flexibility of Kanban. 
This hybrid approach fits the dynamic nature of research and software development in our project.

### Key Features:
- **Work Visualization:** Tasks are managed via a Kanban board on GitHub Projects under title of: AML-Drug-Generation , with columns like Backlog, To Do, In Progress, and Done.
- **Use 10-days sprints** (short-term cycles to complete specific tasks).
- **Sprint Planning:** We hold weekly sprint planning meetings to prioritize tasks, set goals, and adjust workload. <br> At the start of each 2-week sprint, we plan which tasks to tackle.
- **Bi-weekly sprint review** Short Sunday and Tuesday check-ins meeting to synchronize, identify blockers, and align priorities.  
- **WIP Limits:** We cap the number of ongoing tasks to maintain focus and avoid overload.  
- **Continuous Improvement:** At the end of each sprint, we review progress and processes, adjusting practices for better efficiency.  
- **Flexibility:** Scrumban allows us to react quickly to research findings, experimental results, or deployment issues, while maintaining steady progress.

---

## Deliverables
1. Pipeline for patient-specific molecule generation  
2. Target-driven filtering system  
3. Web-based Gradio application  
4. Open-source GitHub repository  
5. Technical documentation and performance report  
6. Research paper for publication  

---

## Why This Matters
This project contributes to the emerging field of AI-powered **precision medicine** by integrating omics data, generative modeling, and pharmacological filters to design truly **patient-specific treatments**. It bridges modern machine learning with molecular biology for translational healthcare impact.

---

## Graduation Project Logbook


We maintain a detailed project logbook to document the progress, challenges, solutions, and key decisions throughout the project lifecycle. 
This continuous documentation helps with transparency, knowledge sharing, and future reference.

The journal is updated regularly by all team members and accessible via:

[Project logbook - Online Google Docs.](https://docs.google.com/document/d/1Ifa06sPZ4M2DEvV2iWkmoy1QI_wjMyzjPStyD3mMQ5U/edit?usp=sharing)

Each entry includes:
- Date and author
- Task or milestone description
- Challenges faced and solutions applied
- Next steps or follow-up actions
- Any relevant references or resources

