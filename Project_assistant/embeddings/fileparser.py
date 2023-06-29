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

def read_ics(id):
    filename = f'patientrecords/{str(id)}/patientcalendar.ics'
    with open(filename,'r') as f:
        data = f.read()
        return str(data)


def read_json(id):
    filename = f'patientrecords/{str(id)}/patientdata.json'
    with open(filename,'r') as f:
        data = json.load(f)
        return str(data)

