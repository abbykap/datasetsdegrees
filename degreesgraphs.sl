#!/bin/bash
#SBATCH --job-name=process_files  
#SBATCH -A gen150   # Job name
#SBATCH --output=output_%j.txt       
#SBATCH --error=error_%j.txt        
#SBATCH --nodes=1                   
#SBATCH --time=02:00:00             
#SBATCH --partition=batch         
rm error*
rm output*
module load cray-python  
module load py-pip
pip install matplotlib pandas
python degreesgraphs.py
