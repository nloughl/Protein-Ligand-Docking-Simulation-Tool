import argparse
import os
import glob
import re
from vina import Vina
import pandas as pd
from pathlib import Path

def run_docking(protein_file, ligand_file, output_dir, center, box_size, exhaustiveness=8, max_poses=10):
    """Run docking with Vina."""
    try:
        v = Vina(sf_name='vina')
        v.set_receptor(protein_file)
        v.set_ligand_from_file(ligand_file)
        v.compute_vina_maps(center=center, box_size=box_size)
        v.dock(exhaustiveness=exhaustiveness, n_poses=max_poses)
        energies = []
        # Get poses as a string
        poses_str = v.poses()
        # Debug: Inspect pose output
        print(f"Raw poses for {ligand_file}: {poses_str[:500]}...")  # Print first 500 chars for brevity
        # Parse REMARK VINA RESULT lines
        pose_pattern = re.compile(r'REMARK VINA RESULT:\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)')
        for i, match in enumerate(pose_pattern.finditer(poses_str), 1):
            if i > max_poses:
                break
            energy, rmsd_lb, rmsd_ub = map(float, match.groups())
            energies.append([i, energy, rmsd_lb, rmsd_ub])
        if not energies:
            print(f"No valid pose data found in Vina output for {ligand_file}")
        output_pdbqt = os.path.join(output_dir, f"docked_{os.path.basename(ligand_file)}")
        v.write_poses(output_pdbqt)
        return energies
    except Exception as e:
        print(f"Error docking {ligand_file}: {e}")
        return []

def save_results(energies, ligand_file, output_dir):
    """Save docking results to CSV."""
    os.makedirs(output_dir, exist_ok=True)
    df = pd.DataFrame(energies, columns=['Pose', 'Affinity (kcal/mol)', 'RMSD l.b.', 'RMSD u.b.'])
    base_name = os.path.basename(ligand_file).replace('.pdbqt', '')
    output_csv = os.path.join(output_dir, f'{base_name}_scores.csv')
    df.to_csv(output_csv, index=False)
    return output_csv

def main():
    """Main function for docking script."""
    parser = argparse.ArgumentParser(description='Run protein-ligand docking with AutoDock Vina.')
    parser.add_argument('--protein', required=True, help='Protein PDBQT file')
    parser.add_argument('--ligand_dir', default='data', help='Directory with ligand PDBQT files')
    parser.add_argument('--output_dir', required=True, help='Output directory for results')
    parser.add_argument('--center', nargs=3, type=float, required=True, help='Docking box center (x y z)')
    parser.add_argument('--box_size', nargs=3, type=float, required=True, help='Docking box size (x y z)')
    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.protein):
        raise FileNotFoundError(f"Protein file {args.protein} not found")
    if not os.path.exists(args.ligand_dir):
        raise FileNotFoundError(f"Ligand directory {args.ligand_dir} not found")

    # Process ligands, excluding protein file and docked output files
    ligand_files = [
        f for f in glob.glob(os.path.join(args.ligand_dir, '*.pdbqt'))
        if f != args.protein and not os.path.basename(f).startswith('docked_')
    ]
    if not ligand_files:
        raise FileNotFoundError(f"No valid ligand PDBQT files found in {args.ligand_dir}")

    for ligand_file in ligand_files:
        print(f"Docking {ligand_file}...")
        energies = run_docking(args.protein, ligand_file, args.center, args.box_size)
        if energies:
            output_csv = save_results(energies, ligand_file, args.output_dir)
            print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    main()