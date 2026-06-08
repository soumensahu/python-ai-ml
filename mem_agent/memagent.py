from mem0 import Memory
import os
from openai import OpenAI
import json
os.environ["OPENROUTER_API_KEY"] = "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"
os.environ["NEO_USERNAME"] = "a82fe277"
os.environ["NEO_PASSWORD"] = "uWOmU3resBMMKrbFBSpvHF_nGUUkjxzJTBh8KsDb_zg"
os.environ["NEO_URL"] = "neo4j+s://a82fe277.databases.neo4j.io"
config={
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config":{
            "model": "nvidia/llama-nemotron-embed-vl-1b-v2:free",
            "api_key":os.environ["OPENROUTER_API_KEY"]  ,
            "openai_base_url": "https://openrouter.ai/api/v1" ,
            "embedding_dims": 1536
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "openrouter/owl-alpha",
            "api_key": os.environ["OPENROUTER_API_KEY"],
            "openai_base_url": "https://openrouter.ai/api/v1",
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "username": os.environ["NEO_USERNAME"],
            "password": os.environ["NEO_PASSWORD"],
            "url": os.environ["NEO_URL"],
            "embedding_model_dims": 1536 
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
        }
    },
}
memory_client=Memory.from_config(config)

llm_client=OpenAI(
    api_key=config["llm"]["config"]["api_key"],
    base_url=config["llm"]["config"]["openai_base_url"]
)

while True:
    user_query=input("Enter your query: \n\n\n")
    search_memory=memory_client.search(query=user_query,filters={'user_id': 'memagent'})
    memories=[
        f"ID:{mem.get("id")}\nMemory:{mem.get("memory")}" for mem in search_memory.get("results")
    ]

    print(f"\nFound memories : {memories}")
    SYSTEM_PROMPT=f"""
    Here is the context about the user: {json.dumps(memories)}
    """
    llm_respons=llm_client.chat.completions.create(
    model=config["llm"]["config"]["model"],
    messages=[
            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content":user_query
            }
        ]
    )

    ai_response=llm_respons.choices[0].message.content

    print("====================AI Response===========================\n\n",ai_response)
    memory_payload = f"User said: {user_query}. Assistant replied: {ai_response}"
    
    memory_client.add(
        user_id="memagent",
        messages=[
            {
                "role":"user",
                "content":user_query
            },
            {
                "role":"assistant",
                "content":ai_response
            }
        ]
    )

    print("\n\nchat history has been stored")