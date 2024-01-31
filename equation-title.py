

"""
This code sample shows Prebuilt Read operations with the Azure Form Recognizer client library. 
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import regex as re
import json
import os

"""
 For more information:
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""
endpoint =  os.environ["endpoint"]
key =  os.environ["azformkey"]



def analyze_read():
    # sample document
    formUrl = "CASI_Assignment.pdf"

    file_path = "data.json"
    try:
        with open(file_path, 'r') as file:
            json_dict = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, we'll start with an empty dictionary
        json_dict = {}
#Create client for the App
    client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

# Fetch the pdf details
    with open("CASI_Assignment.pdf", "rb") as pdf:
        poller = client.begin_analyze_document("prebuilt-layout", pdf)
        result = poller.result()


    first_page = result.pages[0]


    title_candidates = []
    
      # Check the first 5 lines
    for i in result.pages:
        for line in i.lines:
            title_candidates.append(line.content)

    word_to_remove = '*'
    title_candidates = list(filter(lambda word: word != word_to_remove, title_candidates))

    joined_string = ' '.join(title_candidates)

    
    pattern = re.compile(r'(\S+)\s+\((\d+\.\d+)\)')

# List to hold matches
    matches = []
    ind = []


    # Search for matches in each string in the list
    for item in title_candidates:
        for match in pattern.finditer(item):
            if  match.group(2) in ind:
                continue
            else:
                ind.append(match.group(2))
            # The first group is the word before, the second group is the pattern like (1.1)
                matches.append((match.group(1), match.group(2)))

    json_dict["Equations"] = matches

    # FIrst word after the number will be the title
    json_dict["Title"] = title_candidates[1]

    print(json_dict)

    with open('data.json', 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)

if __name__ == "__main__":
    analyze_read()


