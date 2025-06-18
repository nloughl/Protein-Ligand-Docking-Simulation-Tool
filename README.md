# Protein-Ligand-Docking-Simulation-Tool
Python script that automates protein-ligand docking and processes results.

Reads protein and ligand files.
Prepares files for docking (e.g., converts formats, sets docking grid).
Runs AutoDock Vina via command-line calls or Python bindings (e.g., vina package).
Parses output to extract binding affinities and saves docked poses.
Optionally, generates visualizations (e.g., PNG images of docked complexes using PyMOL).
  Test the script with sample protein-ligand pairs from public databases like PDBbind or ZINC.


## Installation
### Prerequisites

- [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install)
- [VS Code with WSL extension](https://code.visualstudio.com/docs/remote/wsl)
- [Miniconda (Linux version)](https://docs.conda.io/en/latest/miniconda.html)

### Steps

1. **Download Miniconda for Linux (if not already installed):**

   In your WSL terminal:

   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh

2. ***Restart your shell or source*** 
  ``` bash 
  source ~/.bashrc

3. ***Create new conda environment***

 ***Create Conda Environment**:
   ```bash
   conda create -n docking_env python=3.8 -y
   conda activate docking_env

  **Install Dependencies**:

    conda install -c conda-forge pymol-open-source matplotlib seaborn pandas openbabel autodock-vina -y

  Alternatively, use the provided environment.yml:

    conda env create -f environment.yml
    conda activate docking_env

**Project Structure**

protein_docking_project/
├── data/               # Input protein and ligand files (PDB, PDBQT, etc.)
├── scripts/            # Python or shell scripts for the pipeline
|     ├──run_docking.py: Runs AutoDock Vina docking.
|     ├──visualize_docking.sh: Converts PDBQT to PDB and runs PyMOL visualization.
|     ├──plot_scores.py: Plots binding affinity distributions.
├── results/            # Output docking results (docked_1hsg_ligand.pdbqt, 1hsg_ligand_scores.csv), visualizations         (docked_1hsg_ligand_viz.png), and plots (1hsg_ligand_scores.csv_plot.png).
├── env.yml             # Optional: environment file for conda
├── .gitignore
└── README.md


**Usage**

1. Download Data

Download 1HSG protein and ligand files:

curl -o data/1hsg_protein.pdb https://files.rcsb.org/download/1HSG.pdb
curl -o data/1hsg_ligand.sdf https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/444252/SDF

2. Prepare Files

Convert protein PDB and ligand SDF to PDBQT using OpenBabel:

obabel data/1hsg_protein.pdb -O data/1hsg_protein.pdbqt -h
obabel data/1hsg_ligand.sdf -O data/1hsg_ligand.pdbqt --partialcharge gasteiger -h

3. Run Docking

Dock the 1HSG ligand to the protein using AutoDock Vina:

python scripts/run_docking.py --protein data/1hsg_protein.pdbqt --ligand_dir data --output_dir results --center 15 10 20 --box_size 20 20 20

4. Visualize Docking Results

Generate a PNG image of the docked pose:

./scripts/visualize_docking.sh

To view docking results interactively in PyMOL:

pymol data/1hsg_protein.pdb results/docked_1hsg_ligand.pdb

5. Plot Binding Affinities

Generate a histogram of binding affinities:

python scripts/plot_scores.py

Outputs
  results/docked_1hsg_ligand.pdbqt: Docked ligand poses.
  results/1hsg_ligand_scores.csv: Binding affinities and RMSDs.
  results/docked_1hsg_ligand_viz.png: PyMOL visualization.
  results/1hsg_ligand_scores.csv_plot.png: Affinity distribution plot.
  results/visualization.log: Visualization logs.


