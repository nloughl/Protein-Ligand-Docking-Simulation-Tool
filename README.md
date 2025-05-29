# Protein-Ligand-Docking-Simulation-Tool
A standalone Python script that automates protein-ligand docking and processes results.

Reads protein and ligand files.
Prepares files for docking (e.g., converts formats, sets docking grid).
Runs AutoDock Vina via command-line calls or Python bindings (e.g., vina package).
Parses output to extract binding affinities and saves docked poses.
Optionally, generates visualizations (e.g., PNG images of docked complexes using PyMOL).
  Test the script with sample protein-ligand pairs from public databases like PDBbind or ZINC.
Deliverable: A command-line tool (e.g., run_docking.py) that users can run locally with inputs and get results.

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
  ```bash
  conda create -n docking_env python=3.10
  conda activate docking_env

4. ***Install packages ***
``` bash
conda install -c conda-forge vina openbabel meeko rdkit

## Project Structure

protein_docking_project/
├── data/               # Input protein and ligand files (PDB, PDBQT, etc.)
├── scripts/            # Python or shell scripts for the pipeline
├── results/            # Output docking results
├── env.yml             # Optional: environment file for conda
├── .gitignore
└── README.md


## Usage
```bash
python run_docking.py --protein 1hsg_protein.pdb --ligand 1hsg_ligand.pdb --output_dir results --center 15 10 20 --box_size 20 20 20

