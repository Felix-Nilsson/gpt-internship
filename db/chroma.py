import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from langchain.text_splitter import NLTKTextSplitter

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.fileparser import pdf_to_plaintext

import tiktoken

import json
import re
import nltk

from pathlib import Path
from print_color import print as printc

def get_collection(name:str):
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=f"""{os.path.dirname(os.path.dirname(__file__))}/db/storage""".replace('\\', '/')
    ))

    openai_api_key = os.getenv("OPENAI_API_KEY")

    emb_fn = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=openai_api_key,
                )
    
    collection = client.get_or_create_collection(
            name=name, 
            embedding_function=emb_fn,
            metadata={"hnsw:space": "cosine"}
        )
    return collection


def make_db_patients():
    print("--- Making new Collection: 'patientrecords' ---")
    
    collection = get_collection("patientrecords")
    
    dirs = [ f.path for f in os.scandir("patientrecords") if f.is_dir() ]
    dirs = [d.replace("\\", "/").split("/")[1] for d in dirs]

    n = len(dirs)
    for j, d in enumerate(dirs):
        print(f"[{j+1}/{n}] 'patientrecords': {d} processing ...", end="\r")
        for filetype in ["patientdata.json","patientcalendar.ics"]:
            file_path = f"patientrecords/{d}/{filetype}"

            chunks = []

            with open(file_path, 'r') as f:
               
                if filetype == "patientdata.json":
                    json_obj = json.load(f)
                    chunks = [json_obj[key] for key in json_obj.keys() if key not in ["prescription", "journal"]] #splits json doc into chunks by keys, ~500 tokens
                    if "prescription" in json_obj.keys():
                        chunks += json_obj["prescription"]
                    if "journal" in json_obj.keys():
                        chunks += json_obj["journal"]
                    
                    for i, chunk in enumerate(chunks):

                        collection.add(
                            documents=[str(chunk)],
                            metadatas=[
                                {
                                    "patient":str(d), 
                                    "type":"json", 
                                    "chunk_size": num_tokens_from_string(str(chunk)),
                                    "chunk_index":i 
                                }
                            ],
                            ids=[f"{d}_{i}_json"]
                        )
                
                if filetype == "patientcalendar.ics":
                    pattern = r"BEGIN:VEVENT(.*?)END:VEVENT"
                    matches = re.findall(pattern, f.read(), re.DOTALL)

                    for i,match in enumerate(matches):

                        collection.add(
                            documents=[match],
                            metadatas=[
                                {
                                    "patient":str(d), 
                                    "type":"ics",
                                    "chunk_size": num_tokens_from_string(match), 
                                    "chunk_index":i
                                }
                            ],
                            ids=[f"{d}_{i}_ics"]
                        )
        printc(f"[{j+1}/{n}] 'patientrecords': {d} Done!              ", color="green")
    print("--- Collection Complete!: 'patientrecords' ---")

      
        
def make_db_docs():
    nltk.download("punkt") ## this should be inactive if punkt has been downloaded

    print("--- Making new Collection: 'docs' ---")
    collection = get_collection("docs")
    
    dirs = [ f.path for f in os.scandir("Project3_intranet/data/records") ]
    dirs = [d.replace("\\", "/") for d in dirs]

    n = len(dirs)
    
    for j,d in enumerate(dirs):
        print(f"[{j+1}/{n}] 'docs': {d} processing ...", end="\r")
        pdf = pdf_to_plaintext(d)
        text_splitter = NLTKTextSplitter()
        chunks = text_splitter.split_text(pdf)

        for i, chunk in enumerate(chunks):
                        formatted_filename = d.split("/")[-1]
                        collection.add(
                            documents=[str(chunk)],
                            metadatas=[
                                {
                                    "doc":str(formatted_filename), 
                                    "type":"txt", 
                                    "chunk_size": num_tokens_from_string(str(chunk)),
                                    "chunk_index":i 
                                }
                            ],
                            ids=[f"{formatted_filename}_{i}"]
                        )
        printc(f"[{j+1}/{n}] 'docs': {d} Done!                ", color="green")
    print("--- Collection Complete!: 'docs' ---")


def query_db_doc(query: str,  name: str, n_results: int = 2):
    collection = get_collection(name)
    ans = collection.query(
        query_texts= query,
        n_results= n_results
    )

    return ans

def query_db(query: str, id: str, name:str, n_results: int = 5 ):
    collection = get_collection(name)
    ans = collection.query(
        query_texts= query,
        where={"patient": id},
        n_results=n_results
    )

    return ans


def num_tokens_from_string(string: str, encoding_name: str ="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


#todo: if collection is huge this should be paralellized in e.g. pyspark
def get_biggest_chunk(name:str):
    collection = get_collection(name)

    ans = collection.get(
        include=["metadatas"]
    )
    
    ids = ans['ids']

    max_size = 0
    max_info = {}
    for i in range(len(ids)):
        if ans["metadatas"][i]["chunk_size"] > max_size:
            max_size = ans["metadatas"][i]["chunk_size"]
            max_info = ans["metadatas"][i]
    
    return max_size,max_info


def print_db_summary():
    print("Database summary:")
    for name in ["docs","patientrecords"]:
        collection = get_collection(name)

        ans = collection.get(
            include=["metadatas"]
        )

        n = len(ans["ids"])
        m = get_biggest_chunk(name)
        print(f"\t{name}:\n\tchunks: {n} \n\tbiggest chunk: {m}\n")
    root_directory = Path('db/storage')
    s = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    print(f"Size: ~{round(s/10**6,2)} MB")

#if we add anything here, database may break, please only functions :-)