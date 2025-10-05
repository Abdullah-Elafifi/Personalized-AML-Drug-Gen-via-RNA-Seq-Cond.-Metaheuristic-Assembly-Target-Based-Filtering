import os
import pandas as pd
import numpy as np
import pyvista as pv
from biotite.structure.io.pdb import PDBFile
from biotite.structure import filter_amino_acids
from PIL import Image, ImageDraw, ImageFont

csv_file = "results/proteins_3d/structure_fetch_report.csv"
pdb_dir = r"D:\FCAI\Vol.4\Graduation_Project\Data_Preparation\tcga_protein_pipeline\results\proteins_3d\structures"
img_dir = "results/proteins_3d/images_Point_Cloud"
collage_file = "results/proteins_3d/protein_collage.png"

os.makedirs(img_dir, exist_ok=True)

# Load report
df = pd.read_csv(csv_file)
saved_images = []

for _, row in df.iterrows():
    protein_id = str(row.get("gene", row.get("accession", "unknown")))

    pdb_file = os.path.join(pdb_dir, f"{protein_id}.pdb")
    if not os.path.exists(pdb_file):
        print(f" Skipping {protein_id} (no PDB file at {pdb_file})")
        continue

    try:
        pdb = PDBFile.read(pdb_file)
        atoms = pdb.get_structure()[0]  # first model
        atoms = atoms[filter_amino_acids(atoms)]  # keep only amino acids
        coords = atoms.coord

        # === Handle b-factor (plDDT for AlphaFold structures) ===
        if "bfactor" in atoms.get_annotation_categories():
            scalars = atoms.bfactor
            cmap = "plasma"  # better for plDDT confidence
            clim = [0, 100]  # AlphaFold plDDT range
        else:
            scalars = np.arange(len(coords))
            cmap = "rainbow"
            clim = None

        # Render with PyVista
        plotter = pv.Plotter(off_screen=True)
        plotter.add_points(
            coords,
            scalars=scalars,
            render_points_as_spheres=True,
            point_size=12,
            cmap=cmap,
            clim=clim
        )

        out_path = os.path.join(img_dir, f"{protein_id}.png")
        plotter.show(screenshot=out_path)
        plotter.close()

        # === Add protein name directly onto the saved image ===
        img = Image.open(out_path)
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        text = protein_id
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        except AttributeError:
            text_w, text_h = draw.textsize(text, font=font)

        x = (img.width - text_w) // 2
        y = img.height - text_h - 5
        draw.text((x, y), text, fill=(0, 0, 0), font=font)
        img.save(out_path)

        saved_images.append(out_path)
        print(f" Rendered + labeled {protein_id}")

    except Exception as e:
        print(f" Failed {protein_id}: {e}")

# === Collage (already labeled images) ===
if saved_images:
    imgs = [Image.open(p) for p in saved_images]
    n_cols = 5
    n_rows = (len(imgs) + n_cols - 1) // n_cols

    cell_w, cell_h = 300, 380
    collage = Image.new("RGB", (n_cols * cell_w, n_rows * cell_h), (255, 255, 255))
    draw = ImageDraw.Draw(collage)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    for idx, img in enumerate(imgs):
        img = img.resize((300, 300))
        x = (idx % n_cols) * cell_w
        y = (idx // n_cols) * cell_h
        collage.paste(img, (x, y))

        protein_name = os.path.splitext(os.path.basename(saved_images[idx]))[0]
        try:
            bbox = draw.textbbox((0, 0), protein_name, font=font)
            text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        except AttributeError:
            text_w, text_h = draw.textsize(protein_name, font=font)

        text_x = x + (cell_w - text_w) // 2
        text_y = y + 310
        draw.text((text_x, text_y), protein_name, fill=(0, 0, 0), font=font)

    collage.save(collage_file)
    print(f" Collage saved → {collage_file}")
else:
    print(" No protein images generated.")
