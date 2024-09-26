#!/bin/bash
#SBATCH --job-name=process_files  
#SBATCH -A gen150   # Job name
#SBATCH --output=powersystem.out       
#SBATCH --error=powersystem.err       
#SBATCH --nodes=1                   
#SBATCH --time=02:00:00             
#SBATCH --partition=batch         

module load cray-python  
module load py-pip
pip install matplotlib pandas
python degreesgraphs2.py
