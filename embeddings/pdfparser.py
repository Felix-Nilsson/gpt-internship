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
    for i in range(3):
        adr = f'mockdata/patientrecords/patientrecord_{i}.pdf'
        text = pdf_to_plaintext(adr)
        print(text + "\n")

read_records()