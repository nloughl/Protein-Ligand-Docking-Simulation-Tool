import pymol
from pymol import cmd
import os
import glob
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def visualize_docking(protein_path, ligand_path, output_dir, ligand_resname="MK1"):
    try:
        logger.info(f"Processing: protein={protein_path}, ligand={ligand_path}")
        if not os.path.exists(protein_path):
            raise FileNotFoundError(f"Protein file not found: {protein_path}")
        if not os.path.exists(ligand_path):
            raise FileNotFoundError(f"Ligand file not found: {ligand_path}")
        
        pymol.finish_launching(["pymol", "-q"])
        cmd.load(protein_path, "protein")
        cmd.load(ligand_path, "ligand")
        
        cmd.show("cartoon", "protein and chain A")
        cmd.show("sticks", f"ligand and resn {ligand_resname}")
        
        ligand_atoms = cmd.count_atoms(f"ligand and resn {ligand_resname}")
        logger.info(f"Ligand atoms selected: {ligand_atoms}")
        if ligand_atoms == 0:
            logger.warning(f"No atoms for resn {ligand_resname}. Using generic selection.")
            cmd.show("sticks", "ligand and not resn HOH")
        
        cmd.zoom()
        cmd.set("ray_trace_frames", 1)
        cmd.set("ray_shadow", 0)
        
        base_name = os.path.splitext(os.path.basename(ligand_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_viz.png")
        cmd.png(output_path, width=800, height=600, dpi=300, ray=1)
        logger.info(f"Saved PNG: {output_path}")
        
        cmd.delete("all")
        
    except Exception as e:
        logger.error(f"Error processing {ligand_path}: {str(e)}")
        raise
    finally:
        pymol.finish_launching(["pymol", "-q"])

if __name__ == "__main__":
    data_dir = "data"
    results_dir = "results"
    output_dir = "results"
    
    try:
        complexes = {
            "1hsg": {"protein": "1hsg_protein", "ligand_resname": "UNL"}
        }
        
        for pdb_id, info in complexes.items():
            protein_file = os.path.join(data_dir, f"{info['protein']}.pdb")
            ligand_file = os.path.join(results_dir, f"docked_{pdb_id}_ligand.pdb")
            
            if os.path.exists(protein_file) and os.path.exists(ligand_file):
                visualize_docking(protein_file, ligand_file, output_dir, info["ligand_resname"])
            else:
                logger.error(f"Skipping {pdb_id}: Missing files (protein={protein_file}, ligand={ligand_file})")
                
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        exit(1)