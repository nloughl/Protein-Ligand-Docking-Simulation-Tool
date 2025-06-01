from vina import Vina
import os
import argparse
import pandas as pd

def prepare_files(protein_file, ligand_file, output_dir):
    """Prepare protein and ligand files for docking (convert to PDBQT if needed)."""
    # For simplicity, assume input files are already in PDB format
    # In a full implementation, use tools like OpenBabel to convert SDF to PDBQT
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return protein_file, ligand_file

def run_docking(protein_file, ligand_file, output_dir, center, box_size):
    """Run AutoDock Vina docking and save results."""
    # Initialize Vina
    v = Vina(sf_name='vina')
    
    # Set receptor and ligand
    v.set_receptor(protein_file)
    v.set_ligand_from_file(ligand_file)
    
    # Define docking box (center and size in Angstroms)
    v.compute_vina_maps(center=center, box_size=box_size)
    
    # Perform docking
    v.dock(exhaustiveness=8, n_poses=10)
    
    # Save results
    output_pdbqt = os.path.join(output_dir, 'docked_ligand.pdbqt')
    v.write_poses(output_pdbqt)
    
    # Get binding affinities
    energies = v.energies()

    return energies, output_pdbqt

def save_results(energies, output_dir):
    """Save docking scores to a CSV file."""
    df = pd.DataFrame(energies, columns=['Affinity (kcal/mol)', 'RMSD l.b.', 'RMSD u.b.', '???4', '???5'])
    print(df.head())

    output_csv = os.path.join(output_dir, 'docking_scores.csv')
    df.to_csv(output_csv, index=False)
    return output_csv

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Protein-Ligand Docking Tool')
    parser.add_argument('--protein', required=True, help='Protein PDB file')
    parser.add_argument('--ligand', required=True, help='Ligand PDB/SDF file')
    parser.add_argument('--output_dir', default='docking_results', help='Output directory')
    parser.add_argument('--center', nargs=3, type=float, default=[0, 0, 0], help='Docking box center (x, y, z)')
    parser.add_argument('--box_size', nargs=3, type=float, default=[20, 20, 20], help='Docking box size (x, y, z)')
    args = parser.parse_args()
    
    # Prepare files
    protein_file, ligand_file = prepare_files(args.protein, args.ligand, args.output_dir)
    
    # Run docking
    energies, docked_pdbqt = run_docking(protein_file, ligand_file, args.output_dir, args.center, args.box_size)
    
    # Save results
    output_csv = save_results(energies, args.output_dir)
    
    print("Docking complete! Scores saved to {}".format(output_csv))
    print("Docked structure saved to {}".format(docked_pdbqt))

if __name__ == "__main__":
    main()