#!/usr/bin/env python3

## Bioinformatics and Data Handling
## Task 3

# Given a list of variant IDs, using Ensembl API retrieve information about alleles, 
# locations, effects of variants in transcripts, and genes containing the transcripts.

import requests
import sys

# Make HTTP GET requests from API
def fetch_endpoint(server, request, content_type):
	
	# Create URL
    r = requests.get(server + request, headers={"Accept": content_type})
    if not r.ok: # Pulled from GET helper function
        r.raise_for_status()
        sys.exit()
    if content_type == 'application/json':
        return r.json()
    else:
        return r.text


# Build request URL to VEP (Variant Effect Predictor) API
def fetch_variant_info(variant_id):

    server = "https://rest.ensembl.org"
    request = f"/vep/human/id/{variant_id}"
    content_type = "application/json"

    return fetch_endpoint(server, request, content_type)


# Extract required info from VEP response
def parse_variant_info(data):

    results = []
    # Extract basic transcript info
    for variant in data: # Iterate over response list (Variants)
        var_id = variant.get("id", "NA")
        alleles = variant.get("allele_string", "NA")
        location = variant.get("input", "NA")

        # Iterate over effects (new row for each effect)
        for effect in variant.get("transcript_consequences", []):
            gene = effect.get("gene_symbol", "NA")
            gene_id = effect.get("gene_id", "NA")
            transcript_id = effect.get("transcript_id", "NA")
            consequences = ",".join(effect.get("consequence_terms", []))

            results.append({
                "variant_id": var_id,
                "location": location,
                "alleles": alleles,
                "transcript_id": transcript_id,
                "gene_id": gene_id,
                "gene_symbol": gene,
                "effects": consequences
            })

    return results

def main():
    variant_ids = ["rs56116432"]  # example given
    for var_id in variant_ids:
        print(f"\n{var_id}...")
        try:
            data = fetch_variant_info(var_id) # Call API
            parsed = parse_variant_info(data) # Parse response
            for entry in parsed:
                print(entry)
        except Exception as e: # if invalid ID
            print(f"Error retrieving {var_id}: {e}")

if __name__ == "__main__":
    main()
    # minor change to push to github :)
