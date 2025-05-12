#!/usr/bin/env python3

"""
Bioinformatics and Data Handling
Task 3

Given a list of variant IDs, use the Ensembl API to retrieve information about alleles,
locations, effects of variants in transcripts, and genes containing the transcripts.
"""

import requests
import sys


def fetch_endpoint(server, request, content_type):
    """
    Make HTTP GET requests from Ensembl API.

    Args:
        server (str): Base URL of the server.
        request (str): Specific API endpoint request.
        content_type (str): Expected response type (e.g., 'application/json').

    Returns:
        dict or str: Parsed JSON or text response.
    """
    # Create URL
    r = requests.get(server + request, headers={"Accept": content_type})
    if not r.ok:  # Pulled from GET helper function
        r.raise_for_status()
        sys.exit()
    if content_type == 'application/json':
        return r.json()
    else:
        return r.text


def fetch_variant_info(variant_id):
    """
    Build request URL to VEP (Variant Effect Predictor) API and fetch data.

    Args:
        variant_id (str): Ensembl variant ID (e.g., 'rs56116432').

    Returns:
        dict: API response parsed from JSON.
    """
    server = "https://rest.ensembl.org"
    request = f"/vep/human/id/{variant_id}"
    content_type = "application/json"

    return fetch_endpoint(server, request, content_type)


def parse_variant_info(data):
    """
    Extract required info from VEP API response.

    Args:
        data (list): VEP API response for a given variant.

    Returns:
        list of dict: Parsed variant details including transcript effects and gene info.
    """
    results = []
    # Extract basic transcript info
    for variant in data:  # Iterate over response list (Variants)
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
    """
    Main: fetch and display variant annotations from Ensembl API.
    """
    variant_ids = ["rs56116432"]  # example given
    for var_id in variant_ids:
        print(f"\n{var_id}...")
        try:
            data = fetch_variant_info(var_id)  # Call API
            parsed = parse_variant_info(data)  # Parse response
            for entry in parsed:
                print(entry)
        except Exception as e:  # if invalid ID
            print(f"Error retrieving {var_id}: {e}")


if __name__ == "__main__":
    main()
    # minor change to push to github :)
