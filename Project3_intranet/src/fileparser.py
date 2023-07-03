from PyPDF2 import PdfReader
import json

data_dir = "Project3_intranet/data"

def pdf_to_plaintext(filename):
    file = f'{data_dir}/{filename}'

    reader = PdfReader(file)

    num_pages = len(reader.pages)
    text = ""
    for i in range(num_pages):
        page = reader.pages[i]
        text += page.extract_text().replace(" ", "").replace("\n"," ")
    
    return text

def read_ics(filename):
    """Reads .ics files to a string."""

    file = f'{data_dir}/{filename}'
    with open(file,'r') as f:
        data = f.read()
        return str(data)


def read_json(filename):
    """Reads .json files to a string."""

    file = f'{data_dir}/{filename}'
    with open(file,'r') as f:
        data = json.load(f)
        return str(data)

print(pdf_to_plaintext("Hospital Guidelines Visitor Policy.pdf"))