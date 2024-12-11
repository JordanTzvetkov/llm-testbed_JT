# Set the NCBI API Key and Config Path environment variables
# $env:NCBI_API_KEY = "api_key_NCBI.txt"
$env:LLM_TESTBED_CONFIG_PATH = "./config.json"


# Step1: Download papers in JSON format
# Step2: convert from JSON to plaintext
#

# Define the path to the Python script and the PMID list

$getPaperJson = "getPaperJSON.py"
$getTextFromJson = "getTextFromJSON.py"
$getPaperSpecies = "getPaperSpecies.py"
$getPaperGenes = "getPaperGenes.py"

$pmidListFile = "./PMID_lists/training_set_unique_pmids.txt"


# Check if the PMID list file exists - this should be created from our
# curated set of pmids in the training data

if (-Not (Test-Path $pmidListFile)) {
    Write-Host "PMID list file not found: $pmidListFile"
    # exit 1
}


# Read each PMID from the file and call Noah's Python script to get pdf

Get-Content $pmidListFile | ForEach-Object {
    $pmid = $_.Trim()
    Write-Host $pmid
    if ($pmid -ne "") {
        Write-Host "Downloading JSON for PMID: $pmid"
        try {
            python $getPaperJson $pmid
        } catch {
            Write-Host "Failed to download JSON for PMID: $pmid"
        }

   Start-Sleep -Seconds 5


            Write-Host "Getting Text from JSON"
        try {
            python $getTextFromJson $pmid
        } catch {
            Write-Host "Failed to get paper text from JSON for PMID: $pmid"
        }

    Start-Sleep -Seconds 3

         Write-Host "Getting species for PMID: $pmid"
        try {
            python $getPaperSpecies $pmid
        } catch {
            Write-Host "Failed to get species for PMID: $pmid"
        }

    Start-Sleep -Seconds 3

         Write-Host "Getting genes for PMID: $pmid"
        try {
            python $getPaperGenes $pmid
        } catch {
            Write-Host "Failed to get genes for PMID: $pmid"
        }

        
    }
}