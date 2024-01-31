

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
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""
endpoint =  os.environ["endpoint"]
key =  os.environ["azformkey"]

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])

def analyze_read():
    # sample document
    formUrl = "CASI_Assignment.pdf"

    file_path = "data.json"

    client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open("CASI_Assignment.pdf", "rb") as pdf:
        poller = client.begin_analyze_document("prebuilt-layout", pdf)
        result = poller.result()

    title_candidates = []
    mainfile = []
      # Check the first 5 lines
    for i in result.pages:
        for line in i.lines:
            c1 = line.content
            title_candidates.append(c1)
            word_to_remove = '*'
            title_candidates = list(filter(lambda word: word != word_to_remove, title_candidates))
        mainfile.append(title_candidates)
        title_candidates = []


    word_to_remove = '*'
    #title_candidates = list(filter(lambda word: word != word_to_remove, title_candidates))

    print(mainfile[2])

0
if __name__ == "__main__":
    analyze_read()


