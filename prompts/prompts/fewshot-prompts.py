from openai import OpenAI

client = OpenAI(
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
  api_key="AIzaSyB_LY4_wQImHSxR9bSUHr5ET4vn3ONcwZw",
)
SYSTEM_PROMPT="""
    you should answer only coding related question
      and your name is alexa.

    Rule - strictly follow the output format in json

    output format :{{
        "code":"String" or null,
        "isCodingQuestion":boolean
    }}
    examples:
    Q: what is the result of a+b?
    A: {{"code":null,"isCodingQuestion":false}}

    Q. write a python program to add two numbers.
    A: {{"code:"def add(a,b):
        return a+b","isCodingQuestion":true}}
    """

response=client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role":"system","content":SYSTEM_PROMPT
        }, 
        {
            "role":"user","content":"explain pascal law"
        }
    ]
)
print(response.choices[0].message.content)