# Multi-PDF RAG System

A modular, local Retrieval-Augmented Generation (RAG) system that allows users to upload and query multiple PDF documents using semantic retrieval and a local Large Language Model.

The system stores document information in SQLite, converts PDF content into chunks and embeddings, stores vectors in ChromaDB, retrieves relevant chunks using document-level filtering, and generates answers using a local Qwen LLM through Ollama.

---

## 🚀 Project Overview

This project implements an end-to-end RAG pipeline for querying information from multiple PDF documents.

Instead of sending the entire PDF directly to an LLM, the system follows a retrieval-based approach:

```text
PDF
 ↓
PDF Loader
 ↓
Text Chunking
 ↓
Document Metadata
 ↓
Embeddings
 ↓
ChromaDB
 ↓
Retriever
 ↓
Relevant Context
 ↓
Prompt Template
 ↓
Qwen LLM
 ↓
Answer
```

The project also supports reusing previously processed PDFs without embedding them again.

---

## ✨ Features

- 📄 Upload and process PDF documents
- 📚 Support for multiple PDFs
- 🔍 Semantic similarity-based retrieval
- 🗂️ Document-level filtering using `document_id`
- 💾 SQLite database for document metadata and embedding status
- 🧠 Local embedding generation using Ollama
- 🗃️ ChromaDB vector database
- 🤖 Local Qwen LLM through Ollama
- 🔄 Reuse previously embedded PDFs
- 🧩 Modular project architecture
- 🔒 Fully local RAG pipeline
- 🚫 No external LLM API required for the core workflow

---

## 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │      User        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Main Menu     │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
              Upload PDF                Existing PDF
                    │                           │
                    ▼                           ▼
             Check SQLite                Select document
                    │                           │
                    ▼                           ▼
              Document ID                Document ID
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Retriever     │
                         └────────┬─────────┘
                                  │
                                  ▼
                             ChromaDB
                                  │
                                  ▼
                       Relevant PDF Chunks
                                  │
                                  ▼
                            Context
                                  │
                                  ▼
                         Prompt Template
                                  │
                                  ▼
                           Qwen LLM
                                  │
                                  ▼
                              Answer
```

---

## 🔄 RAG Pipeline

### 1. PDF Loading

PDF documents are loaded using `PyPDFLoader`.

```text
PDF
 ↓
PyPDFLoader
 ↓
LangChain Documents
```

---

### 2. Text Chunking

The extracted document content is split into smaller chunks using `RecursiveCharacterTextSplitter`.

This improves retrieval by allowing the system to search smaller, semantically meaningful pieces of the document.

Current configuration:

```text
Chunk Size   : 200
Chunk Overlap: 20
```

---

### 3. Document Identification

Each PDF is assigned a unique `document_id`.

The ID is generated using SQLite:

```text
SQLite
   ↓
document_id
```

The `document_id` is then added to the metadata of every chunk:

```python
doc.metadata["document_id"] = document_id
```

This allows the retriever to search only within the selected PDF.

For example:

```text
Python.pdf → document_id = 1
Java.pdf   → document_id = 2
DBMS.pdf   → document_id = 3
```

---

### 4. Embeddings

The project uses Ollama embeddings with:

```text
nomic-embed-text
```

Text chunks are converted into vector representations.

```text
Text Chunk
    ↓
Embedding Model
    ↓
Vector
```

---

### 5. Vector Database

The generated embeddings are stored in ChromaDB.

Each stored item contains:

```text
Embedding
Page Content
Metadata
    └── document_id
```

The ChromaDB collection is persisted locally.

---

### 6. Retrieval

When the user asks a question, the retriever searches ChromaDB for the most relevant chunks.

The current configuration retrieves:

```text
Top K = 3
```

The search is also filtered using the selected document's `document_id`.

Example:

```python
filter = {
    "document_id": document_id
}
```

This prevents the system from retrieving information from unrelated PDFs.

---

### 7. Context Construction

The retrieved chunks are combined into a context:

```text
Retrieved Chunk 1
+
Retrieved Chunk 2
+
Retrieved Chunk 3
        ↓
      Context
```

The context is then passed to the prompt template along with the user's question.

---

### 8. Prompt + LLM

The system uses a structured LangChain prompt template.

The prompt contains:

```text
Context
+
User Question
```

The local Qwen model then generates the final response.

Current model:

```text
qwen2.5-coder:3b
```

through Ollama.

---

## 🗄️ Database Design

SQLite is used to maintain document information.

Example schema:

```text
documents
-----------------------------------------
id
path
filename
embedded
```

### Purpose

| Field | Purpose |
|-------|---------|
| `id` | Unique document identifier |
| `path` | Original PDF path |
| `filename` | PDF filename |
| `embedded` | Tracks whether the document has been processed |

SQLite manages document state, while ChromaDB stores the actual vector representations and chunks.

---

## 📁 Project Structure

```text
multi-pdf-rag/
│
├── .gitignore
├── requirements.txt
│
├── rag/
│   ├── app.py
│   └── rag_pipeline.py
│
└── src/
    │
    ├── loader/
    │   └── loader.py
    │
    ├── chunking/
    │   └── chunk.py
    │
    ├── embeddings/
    │   └── embed.py
    │
    ├── vectorstore/
    │   └── vectstore.py
    │
    ├── retriever/
    │   └── reterive.py
    │
    ├── database/
    │   └── database.py
    │
    └── prompt_template/
        └── prompt.py
```

---

## 🛠️ Technologies & Libraries

**Programming Language**
- Python

**RAG / LLM Framework**
- LangChain

**PDF Processing**
- PyPDFLoader
- langchain-community

**Text Splitting**
- RecursiveCharacterTextSplitter
- langchain-text-splitters

**Embeddings**
- Ollama
- nomic-embed-text

**Vector Database**
- ChromaDB
- langchain-chroma

**Large Language Model**
- Qwen 2.5 Coder 3B
- Ollama
- langchain-ollama

**Database**
- SQLite3 (used for document metadata and document processing status)

**Prompting**
- ChatPromptTemplate

**Output Processing**
- StrOutputParser

**Development Tools**
- Python Virtual Environment
- Git
- GitHub
- VS Code

---

## 🧠 Technical Concepts Used

This project helped implement and understand the following concepts:

### Retrieval-Augmented Generation
Understanding how retrieval and generation work together instead of directly asking an LLM to answer from its pretrained knowledge.

### Semantic Search
Converting text into embeddings and searching for semantically relevant chunks.

### Vector Databases
Using ChromaDB to persist and retrieve vector representations.

### Metadata Filtering
Using `document_id` metadata to isolate retrieval to a specific PDF.

### Document Chunking
Breaking large documents into smaller pieces before embedding.

### Prompt Engineering
Designing prompts that provide retrieved context to the LLM.

### Local LLM Inference
Running the LLM locally through Ollama instead of relying on a cloud API.

### Database Management
Using SQLite to maintain document records and processing status.

### Modular Architecture
Separating the RAG pipeline into independent components such as:

```text
Loader
Chunker
Embedding
Vector Store
Retriever
Prompt
Database
LLM
```

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/harshavardhanpatnaik/multi-pdf-rag.git

cd multi-pdf-rag
```

---

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv myvenv
```

Activate it:

```bash
myvenv\Scripts\activate
```

---

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 🦙 Ollama Setup

Install Ollama on your system.

Then download the required models:

```bash
ollama pull nomic-embed-text

ollama pull qwen2.5-coder:3b
```

Make sure Ollama is running before starting the application.

---

## ▶️ Run the Application

From the project root:

```bash
python -m rag.app
```

You will see:

```text
1. Upload PDF
2. Use Existing PDF
3. Exit
```

---

## 💬 Example Usage

### Upload a new PDF

```text
1. Upload PDF
```

Enter the PDF path:

```text
C:\Documents\Python.pdf
```

The system will:

```text
Load PDF
 ↓
Chunk PDF
 ↓
Generate Embeddings
 ↓
Store in ChromaDB
 ↓
Mark document as embedded
 ↓
Create Retriever
```

Then ask a question:

```text
Enter your question:
What is Python?
```

The system retrieves relevant chunks from the selected PDF and generates an answer using Qwen.

---

## 🔁 Existing PDF

If a PDF has already been embedded, the system does not process it again.

Instead:

```text
SQLite
   ↓
Find document
   ↓
Get document_id
   ↓
Create Retriever
   ↓
Query existing vectors
```

This avoids unnecessary re-embedding.

---

## 🧩 Design Decisions

### Why SQLite?

SQLite is used for lightweight document metadata management.

It tracks:

- Document ID
- PDF path
- Filename
- Embedding status

### Why ChromaDB?

ChromaDB provides persistent vector storage and similarity-based retrieval.

### Why `document_id`?

When multiple PDFs are stored in the same vector database, metadata filtering allows the system to retrieve information only from the selected document.

### Why Ollama?

Ollama allows the entire RAG pipeline to run locally without requiring an external LLM API.

---

## 🧪 Current Limitations

This is currently a learning and portfolio-focused RAG implementation.

Some areas that can be improved in future versions include:

- Better chunking strategies
- Hybrid search
- Reranking
- RAG evaluation metrics
- Source/page citations in answers
- Conversation memory
- Streaming responses
- Web-based UI
- Multimodal / image-based PDF understanding
- Improved error handling
- Production deployment
- Authentication and multi-user support

---

## 🚀 Future Improvements

Planned improvements include:

```text
Current RAG
    ↓
Better Retrieval
    ↓
Reranking
    ↓
RAG Evaluation
    ↓
Conversation Memory
    ↓
Multimodal RAG
    ↓
Web Interface
    ↓
Production Deployment
```

---

## 👨‍💻 Development Approach

This project was developed as a hands-on implementation to understand the internal flow of a modular RAG system.

Rather than relying on a single monolithic RAG script, the system was separated into independent components:

```text
PDF Loading
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector Storage
      ↓
Retrieval
      ↓
Prompt Construction
      ↓
LLM Generation
```

The application logic, project structure, database flow, document identification, retrieval filtering, and integration between the components were implemented and tested manually during development.

The project was built primarily as a learning exercise to understand how RAG systems work internally and how individual components interact with each other.

---

## 📚 Key Learning Outcomes

Through this project, I gained practical experience with:

- Building an end-to-end RAG pipeline
- LangChain component integration
- PDF document processing
- Text chunking strategies
- Embedding generation
- Vector database operations
- Semantic retrieval
- Metadata filtering
- SQLite database operations
- Local LLM inference
- Prompt construction
- Modular Python project architecture
- Debugging RAG retrieval issues
- Managing Python dependencies
- Git and GitHub project management

---

## 📜 License

This project is intended primarily for learning, experimentation, and portfolio demonstration.
