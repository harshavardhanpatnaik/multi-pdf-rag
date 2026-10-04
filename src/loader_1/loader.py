from langchain_community.document_loaders import PyPDFLoader

def load(path):
    loader = PyPDFLoader(path)
    docs  = loader.load()
    
    return docs