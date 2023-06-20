import os
import openai
from embeddings.pdfparser import read_records
import pandas as pd

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def make_embedding(text):
    tmp = openai.Embedding.create(
    input=text,
    model="text-embedding-ada-002"
    )
    return tmp['data'][0]['embedding']

def make_embeddings(texts):
    embeddings = [make_embedding(text) for text in texts]
    d = {'text':texts, 'embedding':embeddings}
    return pd.DataFrame(data=d)

#todo: make it react to new content and create new embeddings if so
def make_records():
    path = "Project1_docassist/patientrecords/embedded_data.pkl"
    if os.path.exists(path):
        print("make_embeddings.py: Read from file")
        df = pd.read_pickle(path)
    else:
        print("make_embeddings.py: No file, making new data")
        df = make_embeddings(read_records())
        df.to_pickle(path)
    
    return df
    #return make_embeddings(read_records())

    