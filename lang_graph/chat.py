from typing_extensions import TypedDict,Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
import os

os.environ["OPENROUTER_API_KEY"] = "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"

llm=ChatOpenAI(
    model="openrouter/owl-alpha",
    openai_api_key=os.environ["OPENROUTER_API_KEY"],
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0
)

class State(TypedDict):
    messages:Annotated[list,add_messages]

def chatbot(state:State):
    print("\n\ninside chatbot node",state)
    response=llm.invoke(state.get("messages"))
    print("\n\nllm response : ",response)
    return {"messages":[response]}
def sampleNode(state:State):
    print("\n\ninside sampleNode node",state)
    return {"messages":["this is a testing node"]}


graph_builder=StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("sampleNode",sampleNode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sampleNode")
graph_builder.add_edge("sampleNode",END)

graph=graph_builder.compile()

updated_state=graph.invoke(State({"messages":["Hi i am agent build in langgraph.may I know your details?"]}))

print("\n\nupdated state: ",updated_state)