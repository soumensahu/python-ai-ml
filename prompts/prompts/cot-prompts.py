from openai import OpenAI
import json
client = OpenAI(
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
  api_key="AIzaSyB_LY4_wQImHSxR9bSUHr5ET4vn3ONcwZw",
)


SYSTEM_PROMPT="""
    You are an expert AI assistant in resolving user queries using chain of thoughts.
    you work on START, PLAN and OUTPUT steps.
    You need to first PLAN wht needs to be done.The PLAN can be multiple steps.
    Once you think enough PLAN has been done,finally you can give an OUTPUT.
    Rules:
    -Strictly follow JSON output.
    -only run one steps at a time.
    -the sequence of steps is START(where user give an input),PLAN(that can be multiple time)
    and finally OUTPUT(which is going to be displayed to the user)

    OUTPUT JSON format:
    {"steps":"START" | "PLAN" | "OUTPUT","content":"String"}

    Example:
    START. Hey, can you solve 2+3*5/10
    PLAN:{"steps":"PLAN","content":"seems like user is interested in math problem"}
    PLAN:{"steps":"PLAN","content":"looking at the problem, we should use BODMAS rule"}
    PLAN:{"steps":"PLAN","content":"Yes BODMAS rule is correct to solve this problem"}
    PLAN:{"steps":"PLAN","content":"First we solve 3*5 which is 15, then we solve 15/10 which is 1.5 and finally we add 2+1.5 which is 3.5"}
    OUTPUT:{"steps":"OUTPUT","content":"The answer to the problem is 3.5"}
    """

#message-history=[]




response=client.chat.completions.create(
    model="gemini-3-flash-preview",
    response_format={"type":"json_object"},
    messages=[
        {
            "role":"system","content":SYSTEM_PROMPT
        }, 
        {
            "role":"user","content":"hey,write a code to reverse a string in python"
        },
        {
            "role":"assistant","content":json.dumps({"steps":"PLAN","content":"seems like user is interested in coding problem"})
        }
    ]
)
print(response.choices[0].message.content)