#!/usr/bin/env python3 

## Bioinformatics and Data Handling
## Task 2

# Report the mean target coverage for the intervals grouped by GC% bins. 
# Bin in 10%GC intervals (e.g. >= 0 to < 10; >= 10 to < 20; etc). 
# Note that in the file, GC values range from 0 to 1 rather than percentage.

import csv

def gc_bin(gc_value):
    """
    Convert GC value (0.0–1.0) into 10% bin (e.g., 0.23 -> 20 for 20% bin).
    """
    return int(gc_value * 10) * 10

def parse_coverage_by_gc(file_path):
    """
    Parses the file and calculates mean target coverage per 10% GC bin.
    """
    gc_bins = {}

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            try:
                gc = float(row['%gc'])
                coverage = float(row['mean_coverage'])
                bin_key = gc_bin(gc)

                if bin_key not in gc_bins:
                    gc_bins[bin_key] = []

                gc_bins[bin_key].append(coverage)
            except (ValueError, KeyError):
                continue  # skip malformed lines

    # Compute and return mean coverage per bin
    results = []
    for bin_start in sorted(gc_bins):
        values = gc_bins[bin_start]
        mean_cov = sum(values) / len(values)
        results.append((f"{bin_start}–{bin_start+10}", round(mean_cov, 2)))

    return results

# Example usage
file_path = "Example.hs_intervals.txt"
for bin_label, mean_cov in parse_coverage_by_gc(file_path):
    print(f"GC% bin {bin_label}: Mean Coverage = {mean_cov}")
