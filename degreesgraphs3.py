import os
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

def count_degrees(file_path):
    """Process a single Matrix Market edge list file and return max, min, and average degree."""
    degree_dict = defaultdict(int)

    with open(file_path, 'r') as file:
        for line in file:
            # Skip comment lines and metadata (starting with '%')
            if line.startswith('%'):
                continue
            
            # Skip the matrix size line (likely containing rows, cols, and non-zero entries)
            if len(line.split()) == 3:
                continue  # Skip the metadata line and move to the next
            parts = line.split()
            if len(parts) < 2:
                print(f"Skipping invalid line in {file_path}: {line.strip()}")
                continue
            # Process the actual data lines (assuming they have node1, node2, and optional weight)
            u, v, *_ = line.split()  # Read node1 and node2, ignore any extra columns like weight
            u, v = int(u), int(v)    # Convert node IDs to integers
            
            # Update the degrees for both nodes
            degree_dict[u] += 1
            degree_dict[v] += 1
    
    # Calculate max, min, and average degrees
    degrees = degree_dict.values()  # Get all the degree values
    
    max_degree = max(degrees)  # Maximum degree
    min_degree = min(degrees)  # Minimum degree
    avg_degree = sum(degrees) / len(degrees)  # Average degree
    
    return max_degree, min_degree, avg_degree


def process_multiple_files(directory_path):
    """Process all edge list files in the specified directory and return degrees."""
    results = {}  # To store max, min, and avg degree for each file
    
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".mtx"):  # Filter for Matrix Market files
            file_path = os.path.join(directory_path, filename)
            print(f"Processing {filename}...")

            # Process each file and store the max, min, and avg degrees
            max_degree, min_degree, avg_degree = count_degrees(file_path)
            results[filename] = {
                "max_degree": max_degree,
                "min_degree": min_degree,
                "avg_degree": avg_degree
            }
    
    return results


def write_to_csv(results, output_file):
    """Write the results dictionary to a CSV file."""
    import csv
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'max_degree', 'min_degree', 'avg_degree']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write header
        for filename, degree_info in results.items():
            writer.writerow({
                'filename': filename, 
                'max_degree': degree_info['max_degree'],
                'min_degree': degree_info['min_degree'],
                'avg_degree': degree_info['avg_degree']
            })

def process_directory(main_directory):
    """Process all subdirectories in the main directory."""
    for subdir in os.listdir(main_directory):
        subdir_path = os.path.join(main_directory, subdir)

        # Ensure it's a directory
        if os.path.isdir(subdir_path):
            print(f"\nProcessing directory: {subdir}")

            # Output CSV and PNG file names based on the subdirectory name
            output_csv = f'degree_statistics_{subdir}.csv'
            output_png = f'degree_statistics_{subdir}.png'

            # Process all .mtx files in the current subdirectory
            degree_stats = process_multiple_files(subdir_path)

            # Write the results to a CSV file
            write_to_csv(degree_stats, output_csv)

            # Create and save the bar chart
            df = pd.DataFrame(degree_stats).T
            df.index.name = 'filename'

            fig, ax = plt.subplots(figsize=(10, 6))
            df[['min_degree', 'max_degree', 'avg_degree']].plot(kind='bar', ax=ax)

            # Adding labels and title
            ax.set_ylabel('Degree')
            ax.set_title(f'Min, Max, and Avg Degree for Each File in {subdir}')
            ax.set_xlabel('File')

            # Rotate the x-axis labels for better readability
            plt.xticks(rotation=45, ha='right')

            # Show and save the plot
            plt.tight_layout()
            plt.savefig(output_png)  # Save the plot to a PNG file
            plt.show()

            print(f"Results written to {output_csv} and plot saved to {output_png}")


# Main directory containing all the subdirectories
main_directory = '/lustre/orion/gen150/world-shared/abby-summer24/nawsdatasets/degree_test3'

# Process each subdirectory and generate CSV and PNG files
process_directory(main_directory)
