# NASA MUREP HPC Guide

This guide provides instructions for setting up the environment, starting interactive sessions, managing jobs, and transferring files on the HPC system. All satellite data is downloaded to `/mnt/beegfs/groups/ouri_project/satdata/`.

---

## Environment Setup

Load the required Anaconda module and activate the `nasa-murep` environment:

```bash
module load anaconda3/2023.09-0-gcc-13.2.0-dmzia4k  

source /opt/ohpc/pub/spack/opt/spack/linux-rocky8-x86_64/gcc-13.2.0/anaconda3-2023.09-0-dmzia4k5kqs3plogxdfbu54jtqps54ma/etc/profile.d/conda.sh  
conda activate nasa-murep
```


```bash
conda create -n nasa-murep python=3.11 -y

conda install -c conda-forge satpy pyresample matplotlib numpy xarray cartopy netCDF4 pandas cmocean matplotlib-scalebar glob2 -y
pip install --upgrade "satpy[all]" -y

conda activate nasa-murep

```

---

## Starting an Interactive Session

To start an interactive session on the `shortq7-gpu` partition with 8 CPUs and 64GB of RAM for 6 hours, use the following command:

```bash
srun --ntasks=1 --cpus-per-task=8 --mem=64G --time=06:00:00 --partition=shortq7-gpu --pty bash  
```

---

## Job Management

### Connecting to the HPC System

SSH into the HPC system:

```bash
ssh <username>@athene-login.hpc.fau.edu  
```

### Monitoring Jobs

- View your jobs in the queue:
  ```bash
  squeue -u $USER  
  ```
- Show detailed information about a specific job:
  ```bash
  scontrol show jobid -dd <JOBID>  
  ```
- Check the status of a specific job:
  ```bash
  squeue --job <JOBID>  
  ```
- View job priority:
  ```bash
  squeue --priority | awk 'NR==1 || $1==<JOBID> || NR==FNR{print}'  
  ```
- Count pending jobs with lower priority than a specific job:
  ```bash
  squeue --state=PENDING --sort=P | awk '{print $1}' | grep -B10000 <JOBID> | wc -l  
  ```

### Canceling a Job

Cancel a specific job:

```bash
scancel <JOBID>  
```

---

## Node Information

View detailed information about nodes:

```bash
sinfo -N -l  
```

Display partition and node group information:

```bash
sinfo -o "%P %N %G"  
```

---

## File Transfer

To transfer files from the HPC system to your local machine, use the following `scp` command:

```bash
scp -r <username>@athene-login.hpc.fau.edu:/mnt/beegfs/home/<username>/scratch/<path> <destination>
```

---

## Fixing DOS Line Breaks in Batch Scripts

If you encounter issues with DOS line breaks in your batch scripts, use the following command to fix them:

```bash
sed -i 's/\r//' job_script.sh  
```

---