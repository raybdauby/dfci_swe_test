#!/usr/bin/env python3 

## Bioinformatics and Data Handling
## Task 1, Part 2

# Given a FASTA file with DNA sequences, find 10 most frequent sequences and return the
# sequence and their counts in the file.

# Finds and returns the 10 most frequent DNA sequences in a FASTA file
def frequent_sequences(file_path):
	# Args: file_path (str): Path to the FASTA file.
    # Returns: List of tuples: Each tuple contains (sequence, count)
    sequences = []
    current_seq = []
    
	# Write each sequence to a list
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_seq:
                    sequences.append(''.join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append(''.join(current_seq))

    # Manually count frequencies using a dictionary
    sequence_counts = {}
    for seq in sequences:
        if seq in sequence_counts:
            sequence_counts[seq] += 1
        else:
            sequence_counts[seq] = 1

    # Sort by count in descending order and get top 10
    most_common = sorted(sequence_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return most_common

# Call the function on the sample fasta file    
results = frequent_sequences("sample_files/fasta/sample.fasta")
for seq, count in results:
    print(f"Sequence: {seq}\nCount: {count}\n")