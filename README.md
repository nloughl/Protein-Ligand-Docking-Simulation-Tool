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
1. Install Python 3.8+.
2. Create a virtual environment: `python -m venv docking_env`.
3. Activate it: `source docking_env/bin/activate` (Linux/Mac) or `docking_env\Scripts\activate` (Windows).
4. Install dependencies: `pip install vina biopython numpy pandas`.
5. Install AutoDock Vina: Download from https://github.com/ccsb-scripps/AutoDock-Vina.

## Usage
```bash
python run_docking.py --protein 1hsg_protein.pdb --ligand 1hsg_ligand.pdb --output_dir results --center 15 10 20 --box_size 20 20 20

