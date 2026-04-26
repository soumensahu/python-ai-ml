from openai import OpenAI

client = OpenAI(
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
  api_key="AIzaSyB_LY4_wQImHSxR9bSUHr5ET4vn3ONcwZw",
)
SYSTEM_PROMPT="you should answer only coding related question and your name is alexa."

response=client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role":"system","content":SYSTEM_PROMPT
        }, 
        {
            "role":"user","content":"who are you?"
        }
    ]
)
print(response.choices[0].message.content)