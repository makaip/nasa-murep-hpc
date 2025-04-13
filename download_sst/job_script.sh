#!/bin/bash
#SBATCH --job-name=download_sst
#SBATCH --output=download_sst_%j.log
#SBATCH --error=download_sst_%j.err
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G

# Load necessary modules (if any)
module load python/3.8

# Activate virtual environment (if applicable)
# source /path/to/venv/bin/activate

# Navigate to the script directory
cd /f/Programming/GitHub/nasa-murep-hpc/download_sst

# Run the Python script
python main.py
