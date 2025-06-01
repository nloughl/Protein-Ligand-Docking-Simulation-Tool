import subprocess
import sys
import os

def run_command(command, check=True, shell=True):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, shell=shell, check=check, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        sys.exit(1)

def check_conda():
    """Check if Conda is installed."""
    print("Checking for Conda...")
    try:
        result = run_command("conda --version", check=False)
        if result.returncode == 0:
            print("Conda is installed.")
        else:
            print("Conda not found. Please install Miniconda: https://docs.conda.io/en/latest/miniconda.html")
            sys.exit(1)
    except FileNotFoundError:
        print("Conda not found. Please install Miniconda: https://docs.conda.io/en/latest/miniconda.html")
        sys.exit(1)

def initialize_conda():
    """Initialize Conda for Bash."""
    print("Initializing Conda...")
    run_command("~/miniconda3/bin/conda init bash")
    print("Conda initialized. Please close and reopen your terminal if prompted.")

def create_environment():
    """Create or recreate docking_env with Python 3.10."""
    print("Checking for docking_env...")
    result = run_command("conda env list | grep docking_env", check=False)
    if "docking_env" in result.stdout:
        print("Removing existing docking_env...")
        run_command("conda env remove -n docking_env -y")
    
    print("Creating docking_env with Python 3.10...")
    run_command("conda create -n docking_env python=3.10 -y")

def configure_channels():
    """Add conda-forge and bioconda channels."""
    print("Configuring Conda channels...")
    run_command("conda config --add channels conda-forge")
    run_command("conda config --add channels bioconda")

def install_dependencies():
    """Install dependencies in docking_env."""
    conda_path = "/home/nloughlin/miniconda3/envs/docking_env/bin/conda"
    pip_path = "/home/nloughlin/miniconda3/envs/docking_env/bin/pip"
    
    print("Installing Conda dependencies...")
    run_command(f"{conda_path} install -c conda-forge numpy swig boost-cpp libboost sphinx sphinx_rtd_theme openbabel -y")
    run_command(f"{conda_path} install -c bioconda autodock-vina mgltools -y")
    
    print("Installing pip dependencies...")
    run_command(f"{pip_path} install biopython pandas")

def verify_setup():
    """Verify Python version and Vina installation."""
    print("Verifying setup...")
    python_path = "/home/nloughlin/miniconda3/envs/docking_env/bin/python"
    
    # Check Python version
    result = run_command(f"{python_path} --version", check=False)
    if "Python 3.10" not in result.stdout:
        print("Error: Python 3.10 not found in docking_env.")
        sys.exit(1)
    print("Python 3.10 confirmed.")
    
    # Check Vina module
    result = run_command(f"{python_path} -c \"from vina import Vina; print('Vina is working')\"", check=False)
    if "Vina is working" not in result.stdout:
        print("Error: Vina module not found.")
        sys.exit(1)
    print("Vina module confirmed.")
    
    # Check Vina binary
    result = run_command("~/miniconda3/envs/docking_env/bin/vina --help", check=False)
    if result.returncode != 0:
        print("Warning: Vina binary not found. Copying to project directory...")
        run_command("cp ~/miniconda3/envs/docking_env/bin/vina .")
    print("Setup verification complete.")

def main():
    """Main function to configure docking_env."""
    print("Configuring docking environment for Protein-Ligand Docking Simulation Tool...")
    check_conda()
    initialize_conda()
    create_environment()
    configure_channels()
    install_dependencies()
    verify_setup()
    print("Setup complete! Activate environment with: conda activate docking_env")
    print("Run docking with: python scripts/run_docking.py --protein data/1hsg_protein.pdbqt --ligand data/1hsg_ligand.pdbqt --output_dir results --center 15 10 20 --box_size 20 20 20")

if __name__ == "__main__":
    main()

