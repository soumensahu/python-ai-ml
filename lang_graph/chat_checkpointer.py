from typing_extensions import TypedDict,Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END,MessagesState
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.mongodb import MongoDBSaver
from openai import OpenAI
from typing import Optional
import os
os.environ["OPENROUTER_API_KEY"] = "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"
os.environ["GEMINI_API_KEY"] = "AIzaSyALx5QyizV-1pRpigPnv9k07G7i3gN2i_k"


client=ChatOpenAI(
    model="openrouter/owl-alpha",
    openai_api_key=os.environ["OPENROUTER_API_KEY"],
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0
)

gemini_client=ChatOpenAI(
    model="gemini-3.5-flash",
    openai_api_key=os.environ["GEMINI_API_KEY"],
    openai_api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    temperature=0
)

class State(TypedDict):
    user_query:str
    llm_output:Optional[str]
    is_good:Optional[bool]


def chatbot(state:MessagesState):
    response=gemini_client.invoke(state["messages"])
    return {"messages": response}

def chatbot_gemini(state:State):
    print("\n\nchatbot_gemini node")
    response=gemini_client.invoke(state.get("user_query"))
    state["llm_output"]=response.content
    return state


graph_builder=StateGraph(MessagesState)

graph_builder.add_node("chatbot",chatbot)

graph_builder.add_edge(START,"chatbot")

#graph_builder.add_edge("chatbot",END)


#graph=graph_builder.compile()

    
     

def compile_graph_with_checkpoint(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

DB_URL="mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URL) as checkpointer:
    graph_with_checkpointer=compile_graph_with_checkpoint(checkpointer)
    config = {"configurable": {"thread_id": "fixed_session_123"}}

    previous_state = checkpointer.get_tuple(config)

    input_1 = {"messages": [{"role": "user", "content": "what I am learning?"}]}
    #prety print
    for chunk in graph_with_checkpointer.stream(
        input_1,config,stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()

    #output_1=graph_with_checkpointer.invoke(input_1,config)
    #print("\n\nLLM Response 1:", output_1["messages"][-1].content)

    #input_2 = {"messages": [{"role": "user", "content": "What is my name?"}]}
    #output_2 = graph_with_checkpointer.invoke(input_2, config)
    #print("\n\nLLM Response 2:", output_2["messages"][-1].content)