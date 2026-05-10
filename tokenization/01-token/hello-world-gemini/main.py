from google import genai

client = genai.Client(
    api_key="key"
)


response=client.models.generate_content(
    model="gemini-3-flash-preview", contents="what is the time now in india?"
)

print(response.text)