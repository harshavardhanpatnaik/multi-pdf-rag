from src.database.database import get_connection
from src.loader_1.loader import load
from src.chunking_2.chunk import chunk
from src.embeddings_3.embed import embeddings
from src.vectorstore_4.vectstore import vector_db
from src.retriever_5.reterive import reterive
from src.prompt_template.prompt import prompt
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import os


class RAG:
    def __init__(self):
        self.embeddings = embeddings()
        self.vectorstore = vector_db(self.embeddings)
        self.prompt = prompt()
        self.retreiver = None
        self.model = ChatOllama(model="qwen2.5-coder:3b")
        self.parser = StrOutputParser()
        self.answer = None
        self.document_id = None

    def embedd(self, document_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE documents SET embedded = 1 WHERE id = ?", (document_id,))
        conn.commit()
        conn.close()

    def ingest_pdf(self, pdf_path, document_id):
        docs = load(pdf_path)

        chunks = chunk(docs)
        self.document_id = document_id
        for doc in chunks:
            doc.metadata["document_id"] = self.document_id

        batch_size = 50
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            self.vectorstore.add_documents(batch)
        self.embedd(self.document_id)
        self.retreiver = reterive(self.vectorstore, self.document_id)

    def ask(self, question):

        if self.retreiver is None:
            self.answer = "PLEASE UPLOAD PDF PATH"
            return

        matter = self.retreiver.invoke(question)

        context = "\n\n".join(doc.page_content for doc in matter)

        chain = self.prompt | self.model | self.parser

        answer = chain.invoke({"context": context, "question": question})

        self.answer = answer

    def use_exisiting_pdf(self, document_id):
        self.document_id = document_id
        self.retreiver = reterive(self.vectorstore, document_id)
