import os
import json
import pandas as pd

def extract_data_from_json(json_data):
    """
    Extracts the species name, gene name, and gene identifier from the JSON data.
    Returns a list of dictionaries containing the information.
    """
    extracted_data = []
    try:
        # Check if "getPaperGenes" exists and is successful
        if json_data.get("getPaperGenes", {}).get("success"):
            species_list = json_data["getPaperGenes"]["response"].get("species", [])
            for species in species_list:
                species_name = species.get("name")
                for gene in species.get("genes", []):
                    gene_id = gene.get("identifier")
                    gene_name = gene.get("name")
                    extracted_data.append({
                        "Species Name": species_name,
                        "Gene Name": gene_name,
                        "Gene ID": gene_id
                    })
    except Exception as e:
        print(f"Error processing JSON data: {e}")
    return extracted_data

def process_json_files(directory_path, output_csv):
    """
    Processes each JSON file in the specified directory, extracts information, and saves it to a CSV.
    """
    all_data = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            pmid = filename.replace(".json", "")
            file_path = os.path.join(directory_path, filename)

            with open(file_path, 'r') as file:
                json_data = json.load(file)
                paper_data = extract_data_from_json(json_data)

                # Add PMID to each record and append to all_data
                for record in paper_data:
                    record["PMID"] = pmid
                    all_data.append(record)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(all_data, columns=["PMID", "Species Name", "Gene Name", "Gene ID"])
    df.to_csv(output_csv, index=False)
    print(f"Data successfully saved to {output_csv}")

# Specify directory containing the JSON files and output CSV file path
directory_path = 'caches/status/'
output_csv = 'extended_set_results.csv'

# Run the function
process_json_files(directory_path, output_csv)
