#!/bin/bash
#SBATCH --job-name=nasa_download
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=02:00:00
#SBATCH --partition=shortq7
#SBATCH --output=download_job_%j.log

# Create a single log file in the script's directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$SCRIPT_DIR/download_debug.log"
TIMESTAMP_FORMAT="%Y-%m-%d %H:%M:%S"

# Function to log messages with timestamp
log_message() {
    echo "[$(date +"$TIMESTAMP_FORMAT")] $1" | tee -a "$LOG_FILE"
}

# Start logging
log_message "Starting NASA data download job"
log_message "Job ID: $SLURM_JOB_ID"
log_message "Running on node: $(hostname)"

# Use the full path for the CSV file
CSV_FILE="/mnt/beegfs/home/jpindell2022/projects/nasa-murep/nasa-murep-hpc/download_modis/downloads.csv"
log_message "Using CSV file: $CSV_FILE"

# Load Anaconda module
log_message "Loading Anaconda module..."
module load anaconda3/2023.09-0-gcc-13.2.0-dmzia4k
if [ $? -ne 0 ]; then
    log_message "ERROR: Failed to load Anaconda module"
    exit 1
fi

# Initialize conda
log_message "Initializing conda..."
source /opt/ohpc/pub/spack/opt/spack/linux-rocky8-x86_64/gcc-13.2.0/anaconda3-2023.09-0-dmzia4k5kqs3plogxdfbu54jtqps54ma/etc/profile.d/conda.sh
if [ $? -ne 0 ]; then
    log_message "ERROR: Failed to initialize conda"
    exit 1
fi

# Activate conda environment
log_message "Activating nasa-murep conda environment..."
conda activate nasa-murep
if [ $? -ne 0 ]; then
    log_message "ERROR: Failed to activate conda environment"
    exit 1
fi

# Display Python and environment information
log_message "Python version: $(python --version 2>&1)"
log_message "Conda environment: $(conda info --envs | grep '*' || echo 'No active environment')"
log_message "Current directory: $(pwd)"

# Set the working directory to the script's directory
cd "$SCRIPT_DIR" || {
    log_message "ERROR: Failed to change directory to script location: $SCRIPT_DIR"
    exit 1
}

# Check if main.py exists
SCRIPT_PATH="/mnt/beegfs/home/jpindell2022/projects/nasa-murep/nasa-murep-hpc/download_modis/main.py"
if [ ! -f "$SCRIPT_PATH" ]; then
    log_message "ERROR: main.py not found at $SCRIPT_PATH"
    exit 1
fi

# Run the Python script
log_message "Starting download using main.py..."
python "$SCRIPT_PATH" "$CSV_FILE" 2>&1 | tee -a "$LOG_FILE"
EXIT_CODE=${PIPESTATUS[0]}

# Log completion status
if [ $EXIT_CODE -eq 0 ]; then
    log_message "Download completed successfully"
else
    log_message "Download failed with exit code $EXIT_CODE"
fi

# Deactivate conda environment
conda deactivate
log_message "NASA data download job finished"

exit $EXIT_CODE
