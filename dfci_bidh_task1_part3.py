#!/usr/bin/env python3 

## Bioinformatics and Data Handling
## Task 1, Part 3

# Given a chromosome and coordinates, write a program for looking up its annotation. 
# Keep in mind you'll be doing this annotation millions of times. 
# Output Annotated file of gene name that input position overlaps

import bisect # for efficient searching
import re # regular expressions
import csv # output file


# Parse GTF (Gene Transfer Format) file to extract gene intervals
def parse_gtf(gtf_file):

    # Returns a dictionary: chrom -> list of (start, end, gene_name)
    annotations = {}

    with open(gtf_file, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip(): # skip comment/empty lines
                continue

            # parts = chrom, source, feature, start, end, score, strand, frame, attributes
            parts = line.strip().split('\t') # split by GTF field
            if len(parts) < 9: # skip lines with incorrect number of fields
                continue
            chrom, source, feature, start, end, score, strand, frame, attributes = parts
            start, end = int(start), int(end) 

            # Extract gene_name from attributes
            match = re.search(r'gene_name "([^"]+)"', attributes) # regex capture " "
            gene_name = match.group(1) if match else 'unknown'

            if chrom not in annotations: # initialize this chr
                annotations[chrom] = []

            annotations[chrom].append((start, end, gene_name)) # append gene interval

    # Sort intervals by start for each chromosome
    for chrom in annotations:
        annotations[chrom].sort()
 
    return annotations


# Binary search to find overlapping gene(s)
def find_overlap(chrom_intervals, position):

    starts = [start for start, _, _ in chrom_intervals] # list of gene start coords
    idx = bisect.bisect_right(starts, position) # find gene start to the left of position

    results = []
    for i in range(max(0, idx - 10), idx): # scan nearby intervals for the position
        start, end, gene = chrom_intervals[i] # i = intervals
        if start <= position <= end:
            results.append(gene) # if position is in gene range, append gene name to pos

    return results or ['NA'] # if no gene overlaps position, return NA


def annotate_positions(gtf_annotations, input_positions, output_file):
    with open(input_positions, 'r') as inp, open(output_file, 'w') as out:
        writer = csv.writer(out)
        writer.writerow(['chromosome', 'position', 'gene']) # header row

        for line in inp:
            if not line.strip(): # skip blank lines
                continue
            chrom, pos = line.strip().split('\t') # parse into chr and pos
            pos = int(pos)

            if chrom in gtf_annotations: 
                genes = find_overlap(gtf_annotations[chrom], pos) # run overlap function
                writer.writerow([chrom, pos, ','.join(set(genes))]) # write gene
            else:
                writer.writerow([chrom, pos, 'NA']) # else no gene


# Run functions on sample files
gtf_file = 'sample_files/gtf/hg19_annotations.gtf'
positions_file = 'sample_files/annotate/coordinates_to_annotate.txt'
output_file = 'annotated_output.csv'

gtf_data = parse_gtf(gtf_file) # parse input GTF file
annotate_positions(gtf_data, positions_file, output_file) # annotate positions

print ('Annotated coordinates can be found in', output_file)
