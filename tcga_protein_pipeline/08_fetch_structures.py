import os
import requests
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Download PDBs
def fetch_alphafold(csv_file, out_dir="results/proteins_3d/structures"):
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(csv_file)
    if "Entry" not in df.columns:
        raise ValueError("CSV must contain 'Entry' column with UniProt accessions")

    results = []
    for _, row in df.iterrows():
        accession = str(row["Entry"])
        gene = str(row.get("Unnamed: 0", accession))  # fallback gene name
        url = f"https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v4.pdb"
        save_path = os.path.join(out_dir, f"{gene}_{accession}.pdb")

        r = requests.get(url)
        if r.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(r.content)
            print(f"[OK] Downloaded {gene} ({accession}) → {save_path}")
            results.append({"gene": gene, "accession": accession, "pdb_file": save_path, "status": "downloaded"})
        else:
            print(f"[MISS] No structure for {gene} ({accession})")
            results.append({"gene": gene, "accession": accession, "pdb_file": "", "status": "missing"})

    results_df = pd.DataFrame(results)
    out_csv = "results/proteins_3d/structure_fetch_report.csv"
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    results_df.to_csv(out_csv, index=False)
    print(f" Structure fetch complete → {out_csv}")
    return results_df


# Render PDB to PNG (py3Dmol)
def render_proteins(report_csv, out_dir="results/proteins_3d/images_Point_Cloud"):
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(report_csv)

    for _, row in df.iterrows():
        if row["status"] != "downloaded":
            continue

        gene, accession, pdb_file = row["gene"], row["accession"], row["pdb_file"]
        out_path = os.path.join(out_dir, f"{gene}_{accession}.png")

        # Load structure
        with open(pdb_file, "r") as f:
            pdb_data = f.read()

        # Viewer setup
        viewer = py3Dmol.view(width=800, height=600)
        viewer.addModel(pdb_data, "pdb")
        viewer.setStyle({"cartoon": {"color": "spectrum"}})  # cartoon rainbow
        viewer.zoomTo()

        # Render to PNG
        png_data = viewer.png()
        with open(out_path, "wb") as f:
            f.write(png_data)

        print(f"[IMG] Rendered {gene} ({accession}) → {out_path}")


# Step 3. Combine PNGs into Grid
def combine_images(image_dir="results/proteins_3d/images_Point_Cloud", out_file="results/proteins_3d/all_proteins.png"):
    images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(".png")]
    images.sort()
    n = len(images)
    if n == 0:
        print(" No images_Point_Cloud found to combine.")
        return

    cols = int(math.ceil(math.sqrt(n)))  # auto grid
    rows = math.ceil(n / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))

    for i, img_path in enumerate(images):
        row, col = divmod(i, cols)
        ax = axes[row, col] if rows > 1 else axes[col]
        img = mpimg.imread(img_path)
        ax.imshow(img)
        ax.axis("off")
        name = os.path.splitext(os.path.basename(img_path))[0]
        ax.set_title(name, fontsize=9)

    # Hide unused
    for j in range(i + 1, rows * cols):
        row, col = divmod(j, cols)
        ax = axes[row, col] if rows > 1 else axes[col]
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(out_file, dpi=200)
    plt.close()
    print(f" Combined image saved → {out_file}")


# Main Pipeline
if __name__ == "__main__":
    csv_input = "results/top20_biomarkers_annotated.csv"

    report_df = fetch_alphafold(csv_input)  # Step 1
    render_proteins("results/proteins_3d/structure_fetch_report.csv")  # Step 2
    combine_images()  # Step 3
