from PyPDF2 import PdfReader
import json

def pdf_to_plaintext(filename):
    reader = PdfReader(filename)

    num_pages = len(reader.pages)
    text = ""
    for i in range(num_pages):
        page = reader.pages[i]
        text += page.extract_text().replace(" ", "").replace("\n"," ")
    
    return text

def read_records():
    texts = []
    for i in range(4):
        adr = f'Project1_docassist/patientrecords/patientrecord_{i}.pdf'
        text = pdf_to_plaintext(adr)
        texts.append(text)
    return texts

#todo - make this part of read records
def read_json_records():
    texts = []
    for i in range(6):
        adr = f'Project1_docassist/patientrecords/patientdata_{i}.json'
        text =read_json(adr)
        texts.append(text)
    return texts


def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
        #data = data['patient']
        #data = f.read()
        return str(data)


#print(read_json('Project1_docassist/patientrecords/patientdata_0.json'))
"""
with open("Project1_docassist/patientrecords/patientdata_0.json", "r") as f:
    parsed = json.load(f)
    print("Printed patientdata_0.json from fileparser.py")
    print(json.dumps(parsed, indent=4))"""