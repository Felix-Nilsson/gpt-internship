import os
import openai
from fileparser import pdf_to_plaintext as pdf
import pandas as pd

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def make_embedding(text):
    embedding = openai.Embedding.create(
        input = text,
        model = 'text-embedding-ada-002'
    )
    return embedding['data'][0]['embedding']

def make_emeddings(names):
    texts = [pdf(name) for name in names]
    embeddings = [make_embedding(text) for text in texts]
    d = {'filename':names, 'text':texts, 'embedding':embeddings}
    return pd.DataFrame(data=d)

def make_records():
    """Stores embedded patient records and calendar in a pickle file."""

    pickle_path = f"Project3_intranet/data/pickle/embeddings.pkl"
    
    #patientrecords/112255
    if os.path.exists(pickle_path):
        df = pd.read_pickle(pickle_path)
        
    else: 
        entries = os.scandir('Project3_intranet/data/records')
        names = [entry.name for entry in entries]

        df = pd.DataFrame(make_emeddings(names))
        df.to_pickle(pickle_path)

    return df
