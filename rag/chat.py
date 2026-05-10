from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

api_key = "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"

#embedding model

embeddings = OpenAIEmbeddings(
    model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    check_embedding_ctx_length=False,
    model_kwargs={"encoding_format": "float"},
)

vector_db=QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embeddings
)

#user input
user_query=input("enter the text to serach : ")

#return relevant chunks
serach_result=vector_db.similarity_search(query=user_query)

context="\n\n\n".join([f"page_content: {item.page_content}\n page_number: {item.metadata['page_label']}\nFile_location: {item.metadata['source']}" for item in serach_result])

SYSTEM_PROMPT="""
you are a helpful AI assitant who can answer user query based on available context retrieve from pdf file along with page_content and page number.

you should only answer to user baed on the follwing context and ask user to open the right page number to know more details.

context:
{context}
"""

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key
)

response=client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role":"system","content":SYSTEM_PROMPT
        }, 
        {
            "role":"user","content":user_query
        }
    ]
)

print(f"response: {response.choices[0].message.content}")