"""
Code sample fetches Notes.
"""

from PyPDF2 import PdfReader
import re
import json



def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text

text = extract_text_from_pdf('CASI_Assignment.pdf')
file_path = "data.json"
try:
    with open(file_path, 'r') as file:
        json_dict = json.load(file)
except FileNotFoundError:
    # If the file doesn't exist, we'll start with an empty dictionary
    json_dict = {}



# Further refining the regex pattern to capture years along with a broader context
pattern = r'\[p\. 6\].*?\.'

# Extracting matches and their contexts
matches = re.findall(pattern, text,re.DOTALL)

# Cleaning up the results to present them more clearly
notes = []
for match in matches:
    print(match)
    notes.append(match)

json_dict["Notes"] = notes

print(json_dict)


with open('data.json', 'w') as json_file:
    json.dump(json_dict, json_file, indent=4)



