from langchain_chroma import Chroma

def vector_db(embeddings):
    
    vectorstore =     Chroma(
        embedding_function = embeddings,
        persist_directory="chroma_db"
    )
        
    return vectorstore

