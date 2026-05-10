from openai import OpenAI
import requests
import json
from pydantic import BaseModel,Field
from typing import Optional

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

def get_weather(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%c+%t"
    response=requests.get(url)
    
    if response.status_code==200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"

available_tool={
    "get_weather":get_weather
}

SYSTEM_PROMPT="""

    You are an expert AI assistant in resolving user queries using chain of thoughts.
    you work on START, PLAN and OUTPUT steps.
    You need to first PLAN wht needs to be done.The PLAN can be multiple steps.
    Once you think enough PLAN has been done,finally you can give an OUTPUT.
    You can call a tool if you think it is necessary from the list of available tools.
    For every tool call,you need to wait for the OBSERVE step to get the output from the tool and then you can PLAN again based on the output of the tool.
    Rules:
    -Strictly follow JSON output.
    -only run one steps at a time.
    -the sequence of steps is START(where user give an input),PLAN(that can be multiple time)
    and finally OUTPUT(which is going to be displayed to the user)
    
    OUTPUT JSON format:
    {"steps":"START" | "PLAN" | "OUTPUT" | "TOOL","content":"String" | None,"tool::String","input":"String"}   

    Available tools:
    1. get_weather(city:str) -> str : gives weather information for a city.

    Example 1:
    START. what is the weather in New York?
    PLAN:{"steps":"PLAN","content":"User is interested in weather information of New York"}
    PLAN:{"steps":"PLAN","content":"Let see if we have a tool to get weather information"}
    PLAN:{"steps":"PLAN","content":"We have a tool get_weather(city:str) that can give us weather information for a city"}
    PLAN:{"steps":"TOOL","tool":"get_weather","input":"New York"}   
    PLAN:{"steps":"OBSERVE","tool":"get_weather","output":"The weather in New York is 🌤️ +25°C"
    PLAN:{"steps":"PLAN","content":"I got the information from the tool, now I can give the final output to the user"
    OUTPUT:{"steps":"OUTPUT","content":"The weather in New York is 🌤️ +25°C"}

"""

class MyoutputFormat(BaseModel):
    steps:str=Field(...,description="This can be START, PLAN, OUTPUT,TOOL etc")
    content:Optional[str]=Field(None,description="This is the content for PLAN and OUTPUT steps")
    tool:Optional[str]=Field(None,description="This is the tool name for TOOL step")
    input:Optional[str]=Field(None,description="This is the input param for the tool")
    output:Optional[str]=Field(None,description="This is the output from the tool for OBSERVE step")


print("\n\n\n")
message_history=[
    {
            "role":"system","content":SYSTEM_PROMPT
    }
]

user_query=input("🔤")
message_history.append({"role":"user","content":user_query})

while True:
    response=client.chat.completions.parse(
        model="openai/gpt-oss-120b:free",
        response_format=MyoutputFormat,
        messages=message_history
    )
    raw_result=response.choices[0].message.content
    message_history.append({"role":"assistant","content":raw_result})
    parsed_result=response.choices[0].message.parsed
    print("Parsed Result: ",parsed_result)

    if parsed_result.steps == "START":
        print("Starting LLM loops: ",parsed_result.content)
        continue
    if parsed_result.steps == "TOOL":
        tool_name=parsed_result.tool
        tool_input=parsed_result.input
        print(f"Toll : {tool_name} ,{tool_input}")
        if tool_name=="get_weather":
            tool_output=get_weather(tool_input)
            print(f"Tool Output: {tool_output}")
            message_history.append({"role":"developer","content":json.dumps({"steps":"OBSERVE","tool":tool_name,"output":tool_output})})
        continue

    if parsed_result.steps == "PLAN":
        print("LLM is thinking: ",parsed_result.content)
        continue
    if parsed_result.steps == "OUTPUT":
        print("Final Result",parsed_result.content)
        break

print("\n\n\n")
