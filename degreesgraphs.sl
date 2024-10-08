#!/bin/bash
#SBATCH --job-name=process_files  
#SBATCH -A gen150   # Job name
#SBATCH --output=graph500.out       
#SBATCH --error=graph500.err       
#SBATCH --nodes=1                   
#SBATCH --time=02:00:00             
#SBATCH --partition=batch         

module load cray-python  
module load py-pip
pip install matplotlib pandas
python degreesgraphs.py
