from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk(docs):
    
    textsplitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 20
        )
    
    chunks = textsplitter.split_documents(docs)
    
    return chunks