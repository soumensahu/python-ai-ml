from openai import OpenAI

client = OpenAI(
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
  api_key="AIzaSyB_LY4_wQImHSxR9bSUHr5ET4vn3ONcwZw",
)
response=client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role":"system","content":"you are a expert in maths and only and only answer math related questions"
        }, 
        {
            "role":"user","content":"who are you?"
        }
    ]
)
print(response.choices[0].message.content)