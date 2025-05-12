#!/usr/bin/env python3

"""
Bioinformatics and Data Handling
Task 1, Part 2

Given a FASTA file with DNA sequences, this script finds the 10 most frequent sequences
and returns each sequence along with its count in the file.
"""

def frequent_sequences(file_path):
    """
    Finds and returns the 10 most frequent DNA sequences in a FASTA file.

    Args:
        file_path (str): Path to the FASTA file.

    Returns:
        List[Tuple[str, int]]: List of tuples, each tuple contains a sequence & count.
    """
    sequences = []
    current_seq = []

    # Read and parse sequences from the FASTA file
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

    # Count sequence frequencies
    sequence_counts = {}
    for seq in sequences:
        if seq in sequence_counts:
            sequence_counts[seq] += 1
        else:
            sequence_counts[seq] = 1

    # Get top 10 most frequent sequences
    most_common = sorted(sequence_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return most_common


# Call the function directly
if __name__ == "__main__":
    results = frequent_sequences("sample_files/fasta/sample.fasta")
    for seq, count in results:
        print(f"\nSequence: {seq}\nCount: {count}")
