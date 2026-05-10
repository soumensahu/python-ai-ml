from openai import OpenAI
import json
import requests

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
    {"steps":"START" | "PLAN" | "OUTPUT" | "TOOL","content":"String" | None,"tool":"String","input":"String"}

    Available tools:
    1. get_weather(city:str) -> str : gives weather information for a city. 

    Example 1:
    START. Hey, can you solve 2+3*5/10
    PLAN:{"steps":"PLAN","content":"seems like user is interested in math problem"}
    PLAN:{"steps":"PLAN","content":"looking at the problem, we should use BODMAS rule"}
    PLAN:{"steps":"PLAN","content":"Yes BODMAS rule is correct to solve this problem"}
    PLAN:{"steps":"PLAN","content":"First we solve 3*5 which is 15, then we solve 15/10 which is 1.5 and finally we add 2+1.5 which is 3.5"}
    OUTPUT:{"steps":"OUTPUT","content":"The answer to the problem is 3.5"}


    Example 2:
    START. What is the weather in New York?
    PLAN:{"steps":"PLAN","content":"User is interested in weather information of New York"}
    PLAN:{"steps":"PLAN","content":"Let see if we have a tool to get weather information"}
    PLAN:{"steps":"PLAN","content":"We have a tool get_weather(city:str) that can give us weather information for a city"}
    PLAN:{"steps":"TOOL","tool":"get_weather","input":"New York"}
    PLAN:{"steps":"OBSERVE","tool":"get_weather","output":"The weather in New York is 🌤️ +25°C"}
    PLAN:{"steps":"PLAN","content":"I got the information from the tool, now I can give the final output to the user"}
    OUTPUT:{"steps":"OUTPUT","content":"The weather in New York is 🌤️ +25°C"
    }
    """
print("\n\n\n")
message_history=[
    {
            "role":"system","content":SYSTEM_PROMPT
    }
]
user_query=input("🔤")
message_history.append({"role":"user","content":user_query})
while True:
    response=client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        response_format={"type":"json_object"},
        messages=message_history
    )
    raw_result=response.choices[0].message.content
    message_history.append({"role":"assistant","content":raw_result})
    try:
        parsed_result=json.loads(raw_result)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Raw result: '{raw_result}'")
        break
    print("Parsed Result: ",parsed_result)
   
    if parsed_result.get("steps") == "START":
        print("Starting LLM loops: ",parsed_result.get("content"))
        continue
    if parsed_result.get("steps") == "TOOL":
        tool_name=parsed_result.get("tool")
        tool_input=parsed_result.get("input")
        print(f"Toll : {tool_name} ,{tool_input}")
        if tool_name=="get_weather":
            tool_output=get_weather(tool_input)
            print(f"Tool Output: {tool_output}")
            message_history.append({"role":"developer","content":json.dumps({"steps":"OBSERVE","tool":tool_name,"output":tool_output})})
        continue

    if parsed_result.get("steps") == "PLAN":
        print("LLM is thinking: ",parsed_result.get("content"))
        continue
    if parsed_result.get("steps") == "OUTPUT":
        print("Final Result",parsed_result.get("content"))
        break


print("\n\n\n")