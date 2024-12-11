import pandas as pd
from Bio import Entrez
import time

# functions
def fetch_pubmed_data(pubmed_id):
    Entrez.email = "jt1995@liverpool.ac.uk"  # Replace with your email
    handle = Entrez.efetch(db="pubmed", id=pubmed_id, retmode="xml")
    records = Entrez.read(handle)
    handle.close()

    # Extract information from the XML record
    article = records['PubmedArticle'][0]
    publication_date = article['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']
    journal = article['MedlineCitation']['Article']['Journal']['Title']
    title = article['MedlineCitation']['Article']['ArticleTitle']

    # Extract DOI and PMC ID, and check for free text availability
    article_ids = article['PubmedData']['ArticleIdList']
    doi = None
    pmc_id = None
    free_text_available = "Likely no free text"

    for id in article_ids:
        if id.attributes['IdType'] == 'doi':
            doi = str(id)
        elif id.attributes['IdType'] == 'pmc':
            pmc_id = str(id)
            free_text_available = "Likely Freely Available"  # Assume availability if there is a PMC ID

    # Additional check: look for 'free' or 'open access' in keywords or publication types
    keywords = article['MedlineCitation'].get('KeywordList', [])
    if any("free" in str(keyword).lower() or "open access" in str(keyword).lower() or "full text" in str(keyword).lower()for keyword in keywords):
        free_text_available = "Likely Freely Available"

    # Return data as a dictionary
    return {
        "PMID": pubmed_id,
        "Title": title,
        "Journal": journal,
        "Publication Date": publication_date,
        "DOI": doi,
        "PMC ID": pmc_id,
        "Free Text Availability": free_text_available,
    }


# Function to fetch data for a list of PMIDs and save as a CSV
def fetch_and_save_pubmed_data(pmids, output_filename="pubmed_data.csv"):
    # Initialise an empty df
    all_data = []

    # Loop through each PMID, fetch data, and append to the DataFrame
    for pmid in pmids:
        print(pmid)
        time.sleep(5)
        try:
            data = fetch_pubmed_data(pmid)
            all_data.append(data)
        except Exception as e:
            print(f"Failed to fetch data for PMID {pmid}: {e}")

    # Convert list of dictionaries to df
    df = pd.DataFrame(all_data)

    # Save to CSV
    df.to_csv(output_filename, index=False)
    print(f"Data saved to {output_filename}")


# Read in list of PMIDs from a text file
with open("PMID_lists/pathogen_training_set_pmids.txt", "r") as file:
    all_pmids = [line.strip() for line in file if line.strip()]

# Process and save the data
fetch_and_save_pubmed_data(all_pmids, output_filename="full_pathogen_set_pmid_data.csv")



# pathogens_and_vectros = readlines"PMID_lists/pathogen_and_vector_pmids.txt"
# fetch_and_save_pubmed_data(pmid_list, output_filename="pathogen_and_vector_pmid_data.csv")