#!/usr/bin/env python3 

## Bioinformatics and Data Handling
## Task 1, Part 1

# Recursively find all FASTQ files in a directory and report each file name and the 
# percent of sequences in that file that are greater than 30 nucleotides long.

import os

# Recursively finds all FASTQ files in a directory
def find_fastq_files(directory):
    # Args: directory: The path to the directory to search.
    # Returns: A list of file paths to FASTQ files.
    fastq_files = []
    for root, _, files in os.walk(directory): # iterate tuples
        for file in files:
            if file.endswith((".fastq")):
                fastq_files.append(os.path.join(root, file)) # append full filepath
    return fastq_files

# Calculates the percentage of sequences in a FASTQ file that are longer than the threshold.
def calculate_long_sequence_percentage(file_path, length_threshold=30):    
    total_sequences = 0
    long_sequences = 0

    with open(file_path, 'r') as f: # open file for reading
        lines = f.readlines()

    # Sequences are every 4th line starting from line 2 (index 1)
    for i in range(1, len(lines), 4):
        sequence = lines[i].strip()
        total_sequences += 1
        if len(sequence) > length_threshold:
            long_sequences += 1

    if total_sequences == 0: # avoid dividing by zero
        return 0.0
    return (long_sequences / total_sequences) * 100

# Run the functions together
def main(directory):
    fastq_files = find_fastq_files(directory)
    for file_path in fastq_files:
        percentage = calculate_long_sequence_percentage(file_path)
        print(f"{os.path.basename(file_path)}: {percentage:.2f}% sequences longer than 30 nt")
        
# Call the main function directly        
if __name__ == "__main__":  
	main('sample_files')