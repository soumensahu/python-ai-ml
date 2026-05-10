from openai import OpenAI
from dotenv import load_dotenv

#load_dotenv()
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="key",
)
response=client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role":"user","content":"Hey There"
        }
    ]
)
print(response.choices[0].message.content)