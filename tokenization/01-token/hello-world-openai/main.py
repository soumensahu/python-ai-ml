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