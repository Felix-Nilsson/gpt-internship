import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Project_assistant.embeddings.fileparser import read_ics,read_json

import tiktoken

import json
import re

def get_collection():
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="db/storage"
    ))

    openai_api_key = os.getenv("OPENAI_API_KEY")

    emb_fn = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=openai_api_key,
                )
    
    collection = client.get_or_create_collection(
            name="patientrecords", 
            embedding_function=emb_fn,
            metadata={"hnsw:space": "cosine"}
        )
    return collection


def make_db():
    
    collection = get_collection()
    
    dirs = [ f.path for f in os.scandir("patientrecords") if f.is_dir() ]
    dirs = [d.split("/")[1] for d in dirs]

    for d in dirs:
        for filetype in ["patientdata.json","patientcalendar.ics"]:
            file_path = f"patientrecords/{d}/{filetype}"

            chunks = []

            with open(file_path, 'r') as f:
               
                if filetype == "patientdata.json":
                    json_obj = json.load(f)
                    chunks = [json_obj[key] for key in json_obj.keys()] #splits json doc into chunks by keys, ~500 tokens

                    for i, chunk in enumerate(chunks):

                        collection.add(
                            documents=[str(chunk)],
                            metadatas=[{"patient":str(d), "type":"json", "chunk_size": num_tokens_from_string(str(chunk))}],
                            ids=[f"{d}_{i}_json"]
                        )
                
                if filetype == "patientcalendar.ics":
                    pattern = r"BEGIN:VEVENT(.*?)END:VEVENT"
                    matches = re.findall(pattern, f.read(), re.DOTALL)

                    for chunk,i in enumerate(chunks):

                        collection.add(
                            documents=[chunk],
                            metadatas=[{"patient":str(d), "type":"ics", "chunk_size": num_tokens_from_string(chunk)}],
                            ids=[f"{d}_{i}_ics"]
                        )
                    
                    """tmp = True
                    chunk = []
                    for line in f:
                        #print(line)
                        if line == "BEGIN:VEVENT\n":
                            tmp = True
                            
                        if line == "END:VEVENT\n":
                            tmp = False

                        if tmp:
                            chunk.append(f.readline())
                        
                        if not tmp:
                            chunks.append(chunk)
                            chunk = []

                        if chunk == []:
                            continue"""
                        
                #print(chunks)

      
        

def query_db():
    collection = get_collection()
    ans = collection.query(
        query_texts= "Vilken patient har skolios?",
        n_results=3
    )

    return ans


def num_tokens_from_string(string: str, encoding_name: str ="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


#make_db()
#print(query_db())
print(get_collection().peek())