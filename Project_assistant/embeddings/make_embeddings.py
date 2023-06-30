import os
import openai
from embeddings.fileparser import read_json,read_ics
import pandas as pd

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def make_embedding(text):
    """Embeds a string using ada-002."""

    tmp = openai.Embedding.create(
    input=text,
    model="text-embedding-ada-002"
    )
    return tmp['data'][0]['embedding']

def make_embeddings(texts):
    """Embeds a set of strings and store them together with the original text in a pandas dataframe."""

    embeddings = [make_embedding(text) for text in texts]
    d = {'text':texts, 'embedding':embeddings}
    return pd.DataFrame(data=d)

#todo: make it react to new content and create new embeddings if so
def make_records(identifier):
    """Stores embedded patient records and calendar in a pickle file."""

    path = f"patientrecords/{identifier}/embeddings.pkl"
    
    #patientrecords/112255
    if os.path.exists(path):
        df = pd.read_pickle(path)
        
    else: 
          
        df = pd.concat([
            make_embeddings([read_json(identifier)]),
            make_embeddings([read_ics(identifier)])
        ]
        ) 
        df.to_pickle(path)
    
    return df
    #return make_embeddings(read_records())