######## just noticed we are working with the output of ~160 papers, not all 480+ in the set of pmids

## what if we try getting the papers in another way? we cand get the pdf from pmc if freely available,
## then pass the entire pdf to the model to summarise?


# first lets see what files have successfully processed
# list all .json files in cahces/status/ and strip .json

# read in the list of all pmids of interest in PMID_lists/training_set_unique_pmids.txt

# set the difference - the ones not as .json but in the list have failed

# then try looking at the pubmed webpage for a few individually and figurinbg out how to get the text in xml

# then convert xml to json for consistency?

# if that doesn't work get the pdf

#### investigate what's causing the cases where you have a couple or more pmids pasted next to each other in your training set.


import os
import requests

# Paths to directories and files
status_dir = "caches/status/"
pmid_list_file = "PMID_lists/all_pmids_to_process.txt"
failed_pmids_file = "PMID_lists/failed_pmids_v3.txt"

# # for take 2
# pmid_list_file = "PMID_lists/training_set_unique_pmids_set2_not_in_set1.txt"
# failed_pmids_file = "PMID_lists/failed_pmids_set2.txt"
# Step 1: List successfully processed PMIDs
def get_processed_pmids(status_dir):
    json_files = [f for f in os.listdir(status_dir) if f.endswith(".json")]
    processed_pmids = {os.path.splitext(f)[0] for f in json_files}  # Strip .json extension
    return processed_pmids


# Step 2: Load all PMIDs from the list of interest
def load_all_pmids(pmid_list_file):
    with open(pmid_list_file, "r") as f:
        all_pmids = {line.strip() for line in f if line.strip()}
    return all_pmids


# Step 3: Identify failed PMIDs
def get_failed_pmids(all_pmids, processed_pmids):
    return all_pmids - processed_pmids



# Main function to execute the steps
def main():
    processed_pmids = get_processed_pmids(status_dir)
    all_pmids = load_all_pmids(pmid_list_file)
    failed_pmids = get_failed_pmids(all_pmids, processed_pmids)

    # Write failed PMIDs to a file for reference
    with open(failed_pmids_file, "w") as f:
        for pmid in failed_pmids:
            f.write(f"{str(pmid)}\n")




if __name__ == "__main__":
    main()



    # # Step 4: Attempt to download PDFs from PMC for failed PMIDs
    # def download_pmc_pdf(pmid):
    #     pmc_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmid}/pdf/"
    #     try:
    #         res = requests.get(pmc_url)
    #         if res.status_code == 200:
    #             pdf_path = f"pdfs/{pmid}.pdf"
    #             with open(pdf_path, "wb") as f:
    #                 f.write(res.content)
    #             print(f"Downloaded PDF for PMID {pmid} to {pdf_path}")
    #             return pdf_path
    #         else:
    #             print(f"No freely available PDF for PMID {pmid} on PMC.")
    #             return None
    #     except requests.RequestException as e:
    #         print(f"Error downloading PDF for PMID {pmid}: {e}")
    #         return None
    #
    #
    # # Step 5: Process failed PMIDs
    # def process_failed_pmids(failed_pmids):
    #     if not os.path.exists("pdfs"):
    #         os.makedirs("pdfs")
    #
    #     for pmid in failed_pmids:
    #         print(f"Attempting to download PDF for failed PMID: {pmid}")
    #         pdf_path = download_pmc_pdf(pmid)
    #         if pdf_path:
    #             # Optional: pass the PDF to a summarization model here
    #             # Example: summarize_pdf(pdf_path)
    #             pass

