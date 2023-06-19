#COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDINGS_MODEL = "text-embedding-ada-002"
CHAT_MODEL = 'gpt-3.5-turbo'
TEXT_EMBEDDING_CHUNK_SIZE=300
VECTOR_FIELD_NAME='content_vector'
PREFIX = "medsdoc"  
INDEX_NAME = "med-index"


VECTOR_DIM = 1536 #len(data['title_vector'][0]) # length of the vectors
DISTANCE_METRIC = "COSINE" # distance metric for the vectors (ex. COSINE, IP, L2)
PREFIX = "medsdoc"  

INDEX_NAME = "med-index"
VECTOR_FIELD_NAME='content_vector'