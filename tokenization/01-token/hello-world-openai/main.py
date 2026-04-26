from openai import OpenAI
from dotenv import load_dotenv

#load_dotenv()
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
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