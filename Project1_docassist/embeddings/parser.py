from PyPDF2 import PdfReader
  
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

read_records()