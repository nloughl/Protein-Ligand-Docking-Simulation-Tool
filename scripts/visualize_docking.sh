#!/bin/bash

# visualize_docking.sh
# Automates PDBQT to PDB conversion and PyMOL visualization for docking results

# Exit on error
set -e

# Activate conda environment
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate docking_env

# Directories
DATA_DIR="data"
RESULTS_DIR="results"
LOG_FILE="$RESULTS_DIR/visualization.log"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check for obabel
if ! command -v obabel &> /dev/null; then
    log "ERROR: OpenBabel not found. Install with: conda install -c conda-forge openbabel"
    exit 1
fi

# Check for Python script
VIS_SCRIPT="scripts/visualize_docking.py"
if [ ! -f "$VIS_SCRIPT" ]; then
    log "ERROR: $VIS_SCRIPT not found"
    exit 1
fi

# Complexes to process
COMPLEXES=("1hsg")

# Process each complex
for PDB_ID in "${COMPLEXES[@]}"; do
    log "Processing $PDB_ID"
    
    # Define file paths
    PROTEIN_PDBQT="$DATA_DIR/${PDB_ID}_protein.pdbqt"
    PROTEIN_PDB="$DATA_DIR/${PDB_ID}_protein.pdb"
    LIGAND_PDBQT="$RESULTS_DIR/docked_${PDB_ID}_ligand.pdbqt"
    LIGAND_PDB="$RESULTS_DIR/docked_${PDB_ID}_ligand.pdb"
    
    # Convert protein PDBQT to PDB
    if [ -f "$PROTEIN_PDBQT" ] && [ ! -f "$PROTEIN_PDB" ]; then
        log "Converting $PROTEIN_PDBQT to $PROTEIN_PDB"
        obabel "$PROTEIN_PDBQT" -O "$PROTEIN_PDB" || {
            log "ERROR: Failed to convert $PROTEIN_PDBQT"
            continue
        }
    elif [ ! -f "$PROTEIN_PDB" ]; then
        log "WARNING: $PROTEIN_PDB not found and no PDBQT to convert"
        continue
    fi
    
    # Convert ligand PDBQT to PDB
    if [ -f "$LIGAND_PDBQT" ] && [ ! -f "$LIGAND_PDB" ]; then
        log "Converting $LIGAND_PDBQT to $LIGAND_PDB"
        obabel "$LIGAND_PDBQT" -O "$LIGAND_PDB" || {
            log "ERROR: Failed to convert $LIGAND_PDBQT"
            continue
        }
    elif [ ! -f "$LIGAND_PDB" ]; then
        log "WARNING: $LIGAND_PDB not found and no PDBQT to convert"
        continue
    fi
    
    # Run PyMOL visualization
    log "Running visualization for $PDB_ID"
    python "$VIS_SCRIPT" || {
        log "ERROR: Visualization failed for $PDB_ID"
        continue
    }
    
    # Check output
    VIZ_PNG="$RESULTS_DIR/docked_${PDB_ID}_ligand_viz.png"
    if [ -f "$VIZ_PNG" ]; then
        log "Success: Generated $VIZ_PNG"
    else
        log "WARNING: $VIZ_PNG not generated"
    fi
done

log "Visualization complete"

