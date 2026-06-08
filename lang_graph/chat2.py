from typing_extensions import TypedDict,Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from openai import OpenAI
from typing import Optional
import os
os.environ["OPENROUTER_API_KEY"] = ""
os.environ["GEMINI_API_KEY"] = ""

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


def chatbot(state:State):
    print("\n\nchatbot node")
    response=client.invoke(state.get("user_query"))
    state["llm_output"]=response.content
    return state

def evaluate_response(state:State) ->Literal["chatbot_gemini","end_node"]:
    if False:
        return "end_node"
    return "chatbot_gemini"

def chatbot_gemini(state:State):
    print("\n\nchatbot_gemini node")
    response=gemini_client.invoke(state.get("user_query"))
    state["llm_output"]=response.content
    return state

def end_node(state:State):
    return state

graph_builder=StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("end_node",end_node)
graph_builder.add_node("chatbot_gemini",chatbot_gemini)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",evaluate_response)
graph_builder.add_edge("chatbot_gemini","end_node")
graph_builder.add_edge("end_node",END)

graph=graph_builder.compile()
updated_state=graph.invoke(State({"user_query":"what is 2+2?"}))
print("\n\nupdated state : ",updated_state)