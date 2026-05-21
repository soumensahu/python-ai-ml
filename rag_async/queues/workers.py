from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


api_key = ""

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


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key
)

def process_query(query:str):
    print("Searching chunks",query)
    serach_result=vector_db.similarity_search(query=query)
    context="\n\n\n".join([f"page_content: {item.page_content}\n page_number: {item.metadata['page_label']}\nFile_location: {item.metadata['source']}" for item in serach_result])
    SYSTEM_PROMPT="""
    you are a helpful AI assitant who can answer user query based on available context retrieve from pdf file along with page_content and page number.

    you should only answer to user baed on the follwing context and ask user to open the right page number to know more details.

    context:
    {context}
    """
    
    response=client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role":"system","content":SYSTEM_PROMPT
        }, 
        {
            "role":"user","content":query
        }
    ])
    print(f"response: {response.choices[0].message.content}")
    return response.choices[0].message.content
