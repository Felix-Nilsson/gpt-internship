import os
import openai
from src.embeddings import make_records
import pandas as pd
from scipy import spatial

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

# search function
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 5
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and similarity score, sorted from most similar to least. Cosine similarity is used."""

    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row['filename'], row['text'], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[2], reverse=True)
    names, strings, relatednesses = zip(*strings_and_relatednesses)
    return names[:top_n], strings[:top_n], relatednesses[:top_n]

def return_best_record(query):
    """Finds the similarity between the query and the documents associated with the id."""

    df = make_records()
    return strings_ranked_by_relatedness(query,df,top_n=3)