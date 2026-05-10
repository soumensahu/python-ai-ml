from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os

# pdf loading in python
pdf_path = Path(__file__).parent / "nodejs_tutorial.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# loaded coument chunking
# chunk into smaller size
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks=text_splitter.split_documents(documents=docs)

print(f"chunks: {chunks[1]}")
# vector embedding and store in local vector DB

# chunk vector embeddings
api_key = "key"
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

embeddings = OpenAIEmbeddings(
    model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    check_embedding_ctx_length=False,
    model_kwargs={"encoding_format": "float"},
)


vector_store=QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="learning_rag"
)