from PyPDF2 import PdfReader
import re
import json



def find_unique_figure_references(text):
    # Regular expression pattern for finding "Figure X.Y"
    pattern = re.compile(r'Figure \d+\.\d+')
    # Find all matches in the text
    matches = pattern.findall(text)
    # Convert matches to a set to remove duplicates, then back to a list
    unique_matches = matches
    return unique_matches[0]

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text,reader

# the path to our PDF file
pdf_text,reader = extract_text_from_pdf('CASI_Assignment.pdf')


pattern = r"^\d\.\d.+$"

# Extracting matching lines
sections = re.findall(pattern, pdf_text, re.MULTILINE)
json_dict = {}

section_list = []
# Output extracted text
for i, section in enumerate(sections, 1):
    print(f"Section {i}:{section.strip()}\n")
    str_section = "Section " + str(i) + " "+ section.strip()
    section_list.append(str_section)

json_dict["Section"] = section_list


####################Figures##############################

figure_list = []

pattern = re.compile(r'^Fig.+', re.M)

# Find and store all matching lines
matching_lines = [line for line in pdf_text.split('\n') if pattern.match(line)]
lst = []
# Print or process the matching lines

for line in matching_lines:
    k = find_unique_figure_references(line)
    if k in lst:
        continue
    else:
        lst.append(k)
        print(line)
        figure_list.append(line)

json_dict["Figures"] = figure_list
##########################################TABLE########################################

table_list =[]
pattern = re.compile(r'^Table.+', re.M)

# Find and store all matching lines
matching_lines = [line for line in pdf_text.split('\n') if pattern.match(line)]
lst = []
# Print or process the matching lines
for line in matching_lines:
    print(line)
    table_list.append(line)

json_dict["Tables"] = table_list

print(json_dict)

with open('data.json', 'w') as json_file:
    json.dump(json_dict, json_file, indent=4)