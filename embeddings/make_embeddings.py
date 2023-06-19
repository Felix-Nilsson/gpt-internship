import os
import openai
from pdfparser import read_records
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

def make_records():
    return make_embeddings(read_records())

def save_records():
    df = make_embeddings(read_records())
    df.to_csv("mockdata/patientrecords/embedded_data/embedded_records.csv")

