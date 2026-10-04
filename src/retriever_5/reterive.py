# from embeddings import embeddings
# from vectorstore import vector_db
def reterive(vectot_store,document_id):
    
    retreiver = vectot_store.as_retriever(
        search_kwargs={"k":3,
                        
                        "filter":{"document_id":document_id }
        }
    )
    
    return retreiver

