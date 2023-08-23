import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from langchain.text_splitter import NLTKTextSplitter, RecursiveCharacterTextSplitter

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

def get_client():
     return chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=f"""{os.path.dirname(os.path.dirname(__file__))}/db/storage""".replace('\\', '/')
    ))
     


def make_db_patients():
    """Creates a vector database that stores medical records of patients by scanning the folder of medical records."""

    print("--- Making new Collection: 'patientrecords' ---")
    
    collection = get_collection("patientrecords")

    #Start by finding every patients directory path, and re-format them if user uses windows path style
    
    dirs = [f.path for f in os.scandir("data/patient_records") if f.is_dir() ]
    #print(dirs)
    dirs = [d.replace("\\", "/") for d in dirs]

    

    n = len(dirs)

    #For every directory d we open it and read two files:
    #   * patientdata.json
    #   * patientcalender.ics
    #
    #For the two files we need two corresponding chunking strategies
    #   * patientdata.json: We maintain context by splitting the file into 
    #     the smallest parts of the json file possible that still contains the 
    #     patient ID.
    #     Specifically the parts 'prescription' and 'journal' mentions the ID for
    #     every element in their lists, so they get special treatment.
    #
    #   * patientcalender.ics: We split the document so that one chunk equals
    #     one event in the calendar, which should also have a mention of
    #     patient ID. Since the ICS format has no header/footer, and is just
    #     a list of calendar events this should be a reliable strategy.
    #
    #As usual we attach metadata tags and add to database along the way.

    for j, d in enumerate(dirs):
        print(f"[{j+1}/{n}] 'patientrecords': {d} processing ...", end="\r")

        for filetype in ["patientdata.json","patientcalendar.ics"]:
            file_path = f"{d}/{filetype}"

            chunks = []

            with open(file_path, 'r', encoding='utf-8') as f:
                
                if filetype == "patientdata.json":
                    json_obj = json.load(f)
                    chunks = [json_obj[key] for key in json_obj.keys() if key not in ["prescription", "journal"]] #splits json doc into chunks by keys, ~500 tokens
                    if "prescription" in json_obj.keys():
                        chunks += json_obj["prescription"]
                    if "journal" in json_obj.keys():
                        chunks += json_obj["journal"]
                    
                    for i, chunk in enumerate(chunks):
                        id = d.split("/")[-1]
                        collection.add(
                            documents=[str(chunk)],
                            metadatas=[
                                {
                                    "patient":id, 
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
    """Creates a vector database for the intranet by scanning through the intranet folder."""

    nltk.download("punkt") ## this should be inactive if punkt has been downloaded

    print("--- Making new Collection: 'docs' ---")
    collection = get_collection("docs")
    
    #First, we make a list of paths to all intranet pdfs and re-format them if user uses windows path style
    dirs = [ f.path for f in os.scandir("data/intranet_records") ]
    dirs = [d.replace("\\", "/") for d in dirs]
    
    n = len(dirs)
    
    #For every path d we open the file, split its contents and add the
    #resulting chunks, with the appropriate metadata tags, into the chroma database.
    for j,d in enumerate(dirs):
        print(f"[{j+1}/{n}] 'docs': {d} processing ...", end="\r")
        pdf = pdf_to_plaintext(d)
        #text_splitter = NLTKTextSplitter()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 200,
            chunk_overlap  = 20,
            length_function = num_tokens_from_string,
            add_start_index = True,
        )
        chunks = text_splitter.split_text(pdf)
        formatted_filename = d.split("/")[-1]

        for i, chunk in enumerate(chunks):
                        
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


def query_db_doc(query: str,  name: str, n_results: int = 5):

    collection = get_collection(name)
    ans = collection.query(
        query_texts= query,
        n_results= n_results
    )

    return ans

def query_db_with_id(query: str, id: str, name:str, n_results: int = 5):
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
    """Helper function used in database summary. Finds biggest chunk of text in a collection."""
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

def get_mean_chunk_size(name:str):
    """Helper function used in database summary. Finds the mean chunk size of a text in a collection."""
    collection = get_collection(name)

    ans = collection.get(
        include=["metadatas"]
    )
    
    
    n = collection.count()
    s = 0
    for i in range(n):
        s += ans["metadatas"][i]["chunk_size"]
            
    
    return s/n

def print_db_summary():
    """Gives you a summary of the collections you have with info like size of collections aswell as biggest and mean chunk size."""

    print("Database summary:")
    for c in get_client().list_collections():
        name = c.name
        collection = get_collection(name)

        ans = collection.get(
            include=["metadatas"]
        )

        n = collection.count()
        m = get_biggest_chunk(name)
        mean = get_mean_chunk_size(name)
        print(f"\t{name}:\n\tchunks: {n} \n\tbiggest chunk: {m}\n\tmean chunk size: {mean} \n")
    root_directory = Path('db/storage')
    s = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    print(f"Size: ~{round(s/10**6,2)} MB")


#if we open the database here, database initialization may break, please use only functions :-)

# - Eg remove things like this before initing:
# - print(get_collection("docs").peek())

make_db_docs()