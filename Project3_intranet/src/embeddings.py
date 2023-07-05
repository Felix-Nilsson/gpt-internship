import os
import openai
from src.fileparser import pdf_to_plaintext as pdf
import pandas as pd

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def make_embedding(text):
    embedding = openai.Embedding.create(
        input = text,
        model = 'text-embedding-ada-002'
    )
    return embedding['data'][0]['embedding']

def make_embeddings(names):
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
        current_files = [elem.name for elem in os.scandir("Project3_intranet/data/records")]

        #checks that pickle file is up to date
        #for big datasets this is slow, could maybe swap for faster strategy like bloomfilter
        if set(df["filename"]) != set(current_files):
            print("src/embeddings.py: embeddings.pkl file outdated, removing and generating...")
            os.remove(pickle_path)
            df = pd.DataFrame(make_embeddings(current_files))
            df.to_pickle(pickle_path)
            print("done")
        else:
            print("src/embeddings.py: embeddings.pkl found & up to date")
    else:
        print("src/embeddings.py: embeddings.pkl file not found, generating...") 
        entries = os.scandir('Project3_intranet/data/records')
        names = [entry.name for entry in entries]

        df = pd.DataFrame(make_embeddings(names))
        df.to_pickle(pickle_path)
        print("done")

    return df

make_records()